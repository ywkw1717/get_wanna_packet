import subprocess
import sys
import threading


def start(filename):
    print('----- {} -----'.format(filename))
    cmd = subprocess.getoutput("tshark -r " + filename + " -Y 'tcp.port == 445 and not smb2 and smb contains 00:31:00:39:00:32:00:2e:00:31:00:36:00:38:00:2e:00:35:00:36:00:2e:00:32:00:30 or smb contains 00:31:00:37:00:32:00:2e:00:31:00:36:00:2e:00:39:00:39:00:2e:00:35 or smb_pipe' -T fields -e tcp.stream |sort -un")

    if not cmd:
        print("Not found")
        return
    else:
        print("FOUND!!!")
        cmd_val = cmd.split('\n')

    options = list(map(lambda s: "tcp.stream==" + s, cmd_val))
    option = ' or '.join(options)

    result_file = filename[0:-5] + "_finish.pcap"
    result = subprocess.getoutput("tshark -r ./" + filename + " -Y '" + option + "' -w " + result_file)
    print(result)
    print('finish.\n')


def main():
    args = sys.argv
    try:
        f = open(args[1], 'r')
    except:
        print("Please specify list of pcap file.")
        return

    threads = []
    l = f.readlines()
    for i in l:
        filename = i.rstrip()
        t = threading.Thread(target=start, args=(filename,))
        threads.append(t)
        t.start()


if __name__ == "__main__":
    main()
