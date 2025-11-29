from config import CONFIG
from ftplib import FTP


def pull_bgp_table(filename, filepath=None):
    """
    Pull BGP Table

    connect to localISP FTP server and then pull the latest snapshot of its BGP table

    Note:
    -----
    the download location of this file is configured at the config file

    :param filename: the name of the file to be downloaded from FTP
    :param filepath: the filepath to save the downloaded file (used only in test)
    :return the procedure status (True for success, False for failure)
    """
    ftp_credentials = CONFIG['ftp_process']
    ftp_server_ip = ftp_credentials['server_ip']
    ftp_user = ftp_credentials['user']
    ftp_pass = ftp_credentials['password']

    try:
        ftp = FTP(ftp_server_ip)
        ftp.login(user=ftp_user, passwd=ftp_pass)

        print("pull latest BGP table snapshot...")

        if not filepath:
            filepath = CONFIG['utilities']['bgp_table']

        with open(filepath, "wb") as file:
            ftp.retrbinary(f"RETR {filename}", file.write)

        print("done!")
        ftp.quit()

        return True

    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    print("pull latest bgp table from FTP server...")
    pull_bgp_table('latest_bgp_table.txt')
    print("Done!")
