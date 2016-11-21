# -*- coding: utf-8 -*-
"""test privatePolicy.py."""


from os.path import join

from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext

from xmap.core.privatePolicy import PrivatePolicy
from xmap.utils.assist import private_policy_pipeline


if __name__ == '__main__':
    # define spark function.
    myconf = SparkConf().setAppName(
        "xmap recommendation: crossSim components")
    sc = SparkContext(conf=myconf)
    sqlContext = SQLContext(sc)

    # define parameters.
    path_root = "file:/home/tlin/notebooks/data"
    path_pickle_train = join(path_root, "cache/two_domain/split_data/train")
    path_pickle_test = join(path_root, "cache/two_domain/split_data/test")
    path_pickle_baseline_sim = join(
        path_root, "cache/two_domain/baseline_sim/basesim")
    path_pickle_extended_sim = join(
        path_root, "cache/two_domain/extend_sim/extendsim")
    path_pickle_private_mapped_sim = join(
        path_root, "cache/two_domain/private_mapping/privatemap")
    path_pickle_nonprivate_mapped_sim = join(
        path_root, "cache/two_domain/private_mapping/nonprivatemap")
    path_pickle_userbased_alterEgo = join(
        path_root, "cache/two_domain/cross_sim/user_based_alterEgo")
    path_pickle_itembased_alterEgo = join(
        path_root, "cache/two_domain/cross_sim/item_based_alterEgo")
    path_pickle_alterEgo_sim = join(
        path_root, "cache/two_domain/cross_sim/targetdomain_sim")
    path_pickle_private_policy_sim = join(
        path_root, "cache/two_domain/private_policy/policy_sim")

    # init class.
    private_policy = PrivatePolicy(
        mapping_range=10, privacy_epsilon=0.6, rpo=0.1)

    # load data.
    alterEgo_sim = sc.pickleFile(path_pickle_alterEgo_sim).cache()
    item_based_alterEgo = sc.pickleFile(path_pickle_itembased_alterEgo).cache()
    user_based_alterEgo = sc.pickleFile(path_pickle_userbased_alterEgo).cache()

    user_based_dict_bd = sc.broadcast(user_based_alterEgo.collectAsMap())
    item_based_dict_bd = sc.broadcast(item_based_alterEgo.collectAsMap())

    # start private policy.
    policy_method = "PSA"
    private_policy_sim = private_policy_pipeline(
        private_policy, alterEgo_sim, policy_method)

    private_policy_sim.saveAsPickleFile(path_pickle_private_policy_sim)