## 0-world_wide_web
Learning about SSL termination

### 0-world_wide_web
A script that will display information about subdomains.
It must accept 2 arguments:
* domain:
   * type: string
   * what: domain name to audit
   * mandatory: yes
* subdomain:
   * type: string
   * what: specific subdomain to audit
   * mandatory: no
Output: `The subdomain [SUB_DOMAIN] is a [RECORD_TYPE] record and points 
to [DESTINATION]`
When only the parameter `domain` is provided, display information for its 
subdomains `www`, `lb-01`, `web-01` and `web-02` - in this specific order
