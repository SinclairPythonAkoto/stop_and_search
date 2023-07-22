# Stop and Search API

Enables users to add information when they have been stopped or witnessed a person being stopped by the police.
The information shared can be used by campaigners to hold police to account and for the wider public to use freely.

# MongoDB Installion Guide
I am using a Linux operating system, being ran on **Ubuntu 20.04** on a *WSL* through my Windows machine.  Installing MongoDB can 
vary depending on the operating system you are using, so these steps are for **Ubuntu 20.04**.

**Import the MongoDB GPG Key**
```
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
```

**Add MongoDB repository**
```
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
```

**Update the package lists then install MongoDB**
```
sudo apt update
sudo apt install mongodb-org
```

**Start the MongoDB service and enable it to start on boot**
```
sudo service mongod start
sudo systemctl enable mongod
```

**Verify if MongoDB is running**
```
sudo service mongod status
```

**Access MongoDB Shell & exit**
```
mongo
quit
```