package main

import (
	"flag"
	"fmt"
	"log"
	"net"
	"strings"

	"github.com/spf13/viper"
)

func lookUpIPv4(name string) []string {
	out := make([]string, 0)
	ips, _ := net.LookupIP(name)
	for _, ip := range ips {
		if ipv4 := ip.To4(); ipv4 != nil {
			out = append(out, ipv4.String())
		}
	}
	return out
}

func main() {
	input := flag.String("input", "prometheus.yml", "Path to Prometheus configuration file")
	output := flag.String("output", "prometheus_out.yml", "Path to wirte the updated configuration file")
	flag.Parse()

	// Check that the filename flag is set
	if *input == "" || *output == "" {
		log.Fatalf("error: input and output flag are required")
	}
	// Read the Prometheus configuration file into a map
	viper.SetConfigFile(*input)
	err := viper.ReadInConfig()
	if err != nil {
		log.Fatalf("error reading configuration file: %v", err)
	}
	config := viper.AllSettings()

	scrapeCfgs := config["scrape_configs"].([]interface{})
	for _, scrapeCfg := range scrapeCfgs {
		if scrapeCfg.(map[string]interface{})["job_name"].(string) != "openmldb_components" {
			continue
		}

		staticCfg := scrapeCfg.(map[string]interface{})["static_configs"].([]interface{})

		for _, cfg := range staticCfg {
			targets := cfg.(map[string]interface{})["targets"].([]interface{})
			for i, target := range targets {
				// resolve domain to IP for openmldb_components targets
				parts := strings.Split(target.(string), ":")
				if len(parts) == 2 {
					ips := lookUpIPv4(parts[0])
					// take up the first IP only
					if len(ips) == 0 {
						log.Fatalf("unable to resolve %s", parts[0])
					}
					targets[i] = fmt.Sprintf("%s:%s", ips[0], parts[1])
				}
			}
		}
	}

	// Write the modified configuration back to the file
	viper.Set("scrape_configs", scrapeCfgs)
	viper.WriteConfigAs(*output)
	if err != nil {
		log.Fatalf("error writing configuration file: %v", err)
	}
}
