import datetime
import os
import platform
import signal
import subprocess
import time
import logging


# def run_cmd(cmd_string, timeout=5):
#     # Logger.logger.info("命令为：" + cmd_string)
#     logging.warning("命令为：" + cmd_string)
#     start = datetime.datetime.now()
#     p = subprocess.Popen(cmd_string, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True, close_fds=True,
#                          start_new_session=True)
#
#     formats = 'gbk' if platform.system() == "Windows" else 'utf-8'
#     time_flag = True
#     try:
#         while p.poll() is None and time_flag:
#             line = p.stdout.readline()
#             line = line.strip()
#             if line:
#                 # Logger.logger.info(line.decode(formats))
#                 logging.warning(line.decode(formats))
#                 time.sleep(0.01)
#             now = datetime.datetime.now()
#             if (now - start).seconds > timeout:
#                 time_flag = False
#         # (msg, errs) = p.communicate(timeout=timeout)
#         if p.returncode:
#             code = 4
#             msg = "[ERROR]执行异常"
#         else:
#             code = 2
#             msg = "[INFO]执行成功"
#     except subprocess.TimeoutExpired:
#         # 注意：不能只使用p.kill和p.terminate，无法杀干净所有的子进程，需要使用os.killpg
#         p.kill()
#         p.terminate()
#         os.killpg(p.pid, signal.SIGTERM)
#
#         # 如果开启下面这两行的话，会等到执行完成才报超时错误，但是可以输出执行结果
#         # (outs, errs) = p.communicate()
#         # print(outs.decode('utf-8'))
#
#         code = 4
#         msg = "[ERROR]Timeout Error : Command '" + cmd_string + "' timed out after " + str(timeout) + " seconds"
#     except Exception as e:
#         code = 4
#         msg = "[ERROR]Unknown Error : " + str(e)
#     return code
#
#
# code = run_cmd("E:/Documents/awfulordersystemBackEnd/eyetrack/cs_sample_streams.exe test")
#
# print(code)
#
# time.sleep(6)
#
#
# print(code)
#
# # # get current path(windows)
# # current_path = os.getcwd()
# #
# # cmd_string = "&" + current_path + "\eyetrack\cs_sample_streams.exe test"
# #
# # print("cmd_string: ", cmd_string)
# #
# # p = subprocess.Popen(cmd_string, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True, close_fds=True, start_new_session=True)
# #
# # # sleep 10 seconds
# # sleep(10)
# #
# # # kill the process
# # p.kill()
#
# # main = r"E:\Documents\awfulordersystemBackEnd\eyetrack\cs_sample_streams.exe"  # exe文件的绝对路径
# # a = subprocess.getstatusoutput(main)    # 我这边使用subprocess.getstatusoutput()方法，还是不能直接调用执行exe文件
# # print (a)

print(datetime.datetime.now())
p = subprocess.Popen("E:/Documents/awfulordersystemBackEnd/eyetrack/cs_sample_streams.exe test", stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True, close_fds=True, start_new_session=True)
print(datetime.datetime.now())
# time.sleep(30)
# print(datetime.datetime.now())
os.system("taskkill /f /im cs_sample_streams.exe")
# print(datetime.datetime.now())
# p.kill()
# p.terminate()
# os.killpg(p.pid, signal.SIGTERM)
