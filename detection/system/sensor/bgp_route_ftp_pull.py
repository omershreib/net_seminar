from config import CONFIG
import paramiko
from ftplib import FTP
import os


# # === FTP server details ===
# FTP_SERVER = "203.0.113.1"
# FTP_USER = "ftpuser"
# FTP_PASS = "051295"
# #FTP_PASS = "vbnWgoEbHUzapEGD1KYP"
# FTP_FILENAME = "latest_bgp_table.txt"


def pull_bgp_table_from_ftp(filename):
    ftp = FTP(CONFIG['ftp']['server_ip'])
    ftp.login(user=CONFIG['ftp']['user'], passwd=CONFIG['ftp']['password'])

    print("connected to FTP for pulling")

    with open(filename, "wb") as file:
        # Command for Downloading the file "RETR filename"
        ftp.retrbinary(f"RETR {filename}", file.write)

    ftp.quit()


if __name__ == "__main__":
    print("pull latest bgp table from FTP server...")
    pull_bgp_table_from_ftp('latest_bgp_table.txt')
    print("Done!")
