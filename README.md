# dicom-transfer

Scripts for dicom studies transfer from a PACS to an Orthanc PACS using DIMSE protocol

## Introduction
PACS can communicate together and transfer exams via C-GET requests. 
Another option is to use a third party PACS to request exams to be sent from a source PACS to a specific target PACS (which must be configured). 
This script uses the power of [orthanc](https://orthanc-server.com) via [pyorthanc](https://pypi.org/project/pyorthanc/) 
 to send such requests.

## Global architecture
When a C-MOVE request is performed, only the acknowledgment that it has been taken into consideration is received. It does not provide any information concerning transfer status. PACS send exams in sequential order and have a limited waiting queue, causing occasional C-MOVE requests to be declined even when an acknowledgment is sent.
To avoid this, we synchronise C-MOVE requests by querying orthanc via API call. 

[![](https://mermaid.ink/img/pako:eNp1kFFrgzAQx79KyFOFZozOhyFjUFTWwTpFZU--ZMk5w2oi8aSU2u--aLvaPewekiP3-__vckcqjAQa0Gpn9qLmFslbVmrious_vyxva5Kb3gog6TrMiQbcG_t9JsZIw4VUwjQMLdddBfauPXiEsechZNvkIx4m3WI8vLMKtCz1lF47RNCh0hyV0SSxWHMt_ms3vjp34uzzIsmcf_QaJlvmr_zV7VTkaZzhJS4GsimKlD3e-w9zfdZMZklWbNbv4eJyezN41d5yf_9Bl7QB23Al3RqPY62kWEMDJQ1cKrmbn5b65Li-lRwhlgqNpUHFdx0sKe_R5ActaIC2h18oUtztprlQpx-qU34e)](https://mermaid.live/edit#pako:eNp1kFFrgzAQx79KyFOFZozOhyFjUFTWwTpFZU--ZMk5w2oi8aSU2u--aLvaPewekiP3-__vckcqjAQa0Gpn9qLmFslbVmrious_vyxva5Kb3gog6TrMiQbcG_t9JsZIw4VUwjQMLdddBfauPXiEsechZNvkIx4m3WI8vLMKtCz1lF47RNCh0hyV0SSxWHMt_ms3vjp34uzzIsmcf_QaJlvmr_zV7VTkaZzhJS4GsimKlD3e-w9zfdZMZklWbNbv4eJyezN41d5yf_9Bl7QB23Al3RqPY62kWEMDJQ1cKrmbn5b65Li-lRwhlgqNpUHFdx0sKe_R5ActaIC2h18oUtztprlQpx-qU34e)

In most cases, the network hosting the PACS is not directly accessible; a more realistic configuration could be presented as show below with 3 VPN connections.

[![](https://mermaid.ink/img/pako:eNqNUU9rgzAU_yohJ4VmjM7DkDEoKutgnaJuJy9Z8pxhNZEYKaX2uy9pu9oVBnuH5JHfv5dkh5nigENcr9WGNVQb9JJXEtnqh49PTbsGvfWgkQSzUfrrCLnKIo8LplpiNJV9Dfqm2_roiIPklbxyKdSgGaBsERX_NSPkcYzIKn1PxoPOc4t_HXFOiKE3QlIjlESpNg2V7K84d2rdkbUvyjS3_vFzlK5IMA_ml1OhBzfDU1KOaFmWGbm_De4mfNIczNK8XC5eI--0-xPxrL3k_b4HnuEWdEsFt5-xc1iFTQMtVDi0Lad2flzJveUNHacGEi6M0jis6bqHGaaDUcVWMhwaPcAPKRbUvk17Yu2_AfoGlHs)](https://mermaid.live/edit#pako:eNqNUU9rgzAU_yohJ4VmjM7DkDEoKutgnaJuJy9Z8pxhNZEYKaX2uy9pu9oVBnuH5JHfv5dkh5nigENcr9WGNVQb9JJXEtnqh49PTbsGvfWgkQSzUfrrCLnKIo8LplpiNJV9Dfqm2_roiIPklbxyKdSgGaBsERX_NSPkcYzIKn1PxoPOc4t_HXFOiKE3QlIjlESpNg2V7K84d2rdkbUvyjS3_vFzlK5IMA_ml1OhBzfDU1KOaFmWGbm_De4mfNIczNK8XC5eI--0-xPxrL3k_b4HnuEWdEsFt5-xc1iFTQMtVDi0Lad2flzJveUNHacGEi6M0jis6bqHGaaDUcVWMhwaPcAPKRbUvk17Yu2_AfoGlHs)

## Usefull link

[Understanding DICOM with Orthanc](https://book.orthanc-server.com/dicom-guide.html)

## Requirements

This script requires the following :

- Access to the destination orthanc server (can call `ORTHANC_HOST` url)
- Adding the destination orthanc server in the source PACS server configuration
- A local instance of orthanc. A configuration file with the destination (section `DicomModalities` in `conf/orthanc.config` file) must be prepared. Afterwards, running it via docker is generaly easiest, with, for example: 
```dockerfile
# In this example, you need to place a orthanc.config file in conf directory
docker run -p 8042:8042 -p 4242:4242 -v conf/orthanc.config:/etc/orthanc/orthanc.json:ro --name orthanc jodogne/orthanc-plugins 
```
- The source PACS configured in the local orthanc must be accessible


## Installation
```python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


## Run
```python
source .venv/bin/activate
python main.py
```