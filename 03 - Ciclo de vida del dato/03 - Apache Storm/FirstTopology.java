package com.storm.learn;

import com.storm.learn.FirstBolt;
import org.apache.storm.starter.spout.RandomIntegerSpout;
import org.apache.storm.Config;
import org.apache.storm.LocalCluster;
import org.apache.storm.topology.TopologyBuilder;
import org.apache.storm.StormSubmitter;
import org.apache.storm.generated.AlreadyAliveException;
import org.apache.storm.generated.AuthorizationException;
import org.apache.storm.generated.InvalidTopologyException;


public class FirstStormClusterTopology {
        public static void main(String[] args) {
                // Create an instance of TopologyBuilder class
                TopologyBuilder builder = new TopologyBuilder();
                // Set the Spout class
                builder.setSpout("FirstSpout", new RandomIntegerSpout(), 2);
                // Set the bolt class
                builder.setBolt("FirstBolt", new FirstBolt(), 4).shuffleGrouping("FirstSpout");
                Config conf = new Config();
                //conf.setDebug(true);
                if (args != null && args.length > 0) {
                        conf.setNumWorkers(3);
                        // This statement submit the topology on remote args[0] = name of topology
                        try {
                            StormSubmitter.submitTopology(args[0], conf, builder.createTopology());
                        } catch (AlreadyAliveException alreadyAliveException) {
                            System.out.println(alreadyAliveException);
                        } catch (InvalidTopologyException invalidTopologyException) {
                            System.out.println(invalidTopologyException);
                        } catch (AuthorizationException e) {
                            e.printStackTrace();
                        }
                } else {
                        try {
                            // Create an instance of LocalCluster class for executing topology in local mode
                            LocalCluster cluster = new LocalCluster();
                            // FirstStormClusterTopology is the name of submitted topology
                            cluster.submitTopology("FirstStormClusterTopology", conf, builder.createTopology());
                            Thread.sleep(100000);
                            // Kill the FirstStormClusterTopology
                            cluster.killTopology("FirstStormClusterTopology");
                            // Shutdown the storm test cluster
                            cluster.shutdown();
                        } catch (Exception exception) {
                            System.out.println("Thread interrupted exception : " + exception);
                        }

                }
        }
}
