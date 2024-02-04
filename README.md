# NetworkAppControl-MiniAPI

## How to run

1. To run the miniAPI and make it fully operational, we first need to install some OS-level dependencies:

```bash
sudo apt update

# Install dependencies - iperf3, ss, ping, netstat, and nmap
sudo apt install iperf3 iproute2 iputils-ping net-tools nmap -y 
```

2. Then, clone the repository:

```bash
cd ~
git clone https://github.com/5gasp/NetworkAppControl-MiniAPI.git
cd ~/NetworkAppControl-MiniAPI/
```

3. Now, we need to install the miniAPI requirements. This can be done on the host or using a virtual environment.

* On host:
```bash
sudo apt install python3-pip -y
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

* Using venv:

```bash
sudo apt install python3.10-venv -y
cd ~/NetworkAppControl-MiniAPI/
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

4. Finally, run the miniAPI:

```bash
cd ~/NetworkAppControl-MiniAPI/src
python3 -m uvicorn main:app --host=0.0.0.0  --port=3001 
```

### Run using Docker

1. Docker must be installed on the OS. You can find the official tutorial on how to install Docker [here](https://docs.docker.com/desktop/install/linux-install/).

2. Run:
```bash
cd ~/NetworkAppControl-MiniAPI/
docker compose up
```