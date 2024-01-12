# This is a sample Python script.
import  gp
import argparse
import sys

def printAndFlush(str):
    print(str)
    sys.stdout.flush()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download bam files frm AmpliconSuite jobs",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-j", "--jobnumber", type=int, help="GenePattern job number")
    parser.add_argument("-f", "--fileextension", type=str, help="File extensions to download")
    parser.add_argument("-u", "--userid", type=str, help="GenePattern user_id")
    parser.add_argument("-p", "--userpass", type=str, help="GenePattern password")
    parser.add_argument("-g", "--genepattern", type=str, help="GenePattern server url")

    args = parser.parse_args()
    gpserver = gp.GPServer(args.genepattern, args.userid, args.userpass)
    job = gp.GPJob(gpserver, args.jobnumber)
    files = job.get_output_files()

    skipped_files = list()
    saved_files = list()

    for file in files:
        if file.get_name().endswith(args.fileextension):
            remote_file = job.get_file(file.get_name())
            saved_files.append(file.get_name())
            printAndFlush(f"downloading file... {file.get_name()}")
            response = remote_file.open()
            CHUNK = 16 * 1024 *1024
            with open(file.get_name(), 'wb') as f:
                while True:
                    chunk = response.read(CHUNK)
                    if not chunk:
                        break
                    f.write(chunk)

        else:
            skipped_files.append(file.get_name())

    if len(saved_files) == 0:
        print(f"No files with extension { args.file-extension } found in job { args.job-number } on server {args.genepattern-server-url}")
        print("Available output files for this job are:")
        for afile in skipped_files:
            print(f"     { aFile }")

