#!/bin/bash
ssh -i /root/.ssh/keys/vm root@ldap /root/backup.sh
scp -qi /root/.ssh/keys/vm root@ldap:/root/backups/ldap-backup.ldif.gz /root/backup/
