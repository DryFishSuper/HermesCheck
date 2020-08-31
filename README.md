# HermesCheck
A tool to check whether Hermes products are in stock.
## Usage
* check_proxy_availability.py: Check the proxies in proxy_list whether works and add them to proxy_list_available.csv
* main.py: Replace product sku, from_email, password and to_email in main and run main to start the program checking whether the product is in stock. Setting up a longer sleeping time may reduce probability of being blocked.
## Proxy
There are several free proxy websites providing a lot of proxy ips, but few of them is available and only https can work.
A better way is to launch EC2s on AWS, you can see [this](https://blog.coingecko.com/how-to-create-a-self-healing-web-proxy-cluster-with-aws-and-squid-in-8-steps/) for reference. 
