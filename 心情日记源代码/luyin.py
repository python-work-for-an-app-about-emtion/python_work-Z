import pyaudio  # 语音输入
import wave
from aip import AipSpeech  # 语音识别
import os

# 读取文件
def get_file_content(filePath):   # 调取系统命令修改音频文件格式，由wav转为pcm格式便于百度语音识别
    cmd_str = "ffmpeg -y  -i %s  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 %s.pcm" % (filePath, filePath)
    os.system(cmd_str)  # 调用系统命令ffmpeg,传入音频文件名
    print(filePath)  # 便于查看文件格式修改是否成功
    with open(filePath+".pcm", 'rb') as fp:   # 打开转换格式成功的pcm文件，二进制方式
        return fp.read()    # 返回音频文件数据便于百度语音分析

def luyin():    # 语音输入及语音识别主函数
	APP_ID = '16328975'  # 此为调用百度语音识别服务的账号信息
	API_Key = 'wuHLtlnNUB1OUBAqF6BgwkKc'
	Secret_Key = 'ff3W5nw0gNPmDUwboNvvrd0BxaFA9NyW'

	client = AipSpeech(APP_ID, API_Key, Secret_Key)
	# 以下为语音输入模块
	CHUNK = 1024 # 数据流块
	FORMAT = pyaudio.paInt16  #定义采样值的量化格式
	CHANNELS = 2  # 声道数
	RATE = 16000  # 取样频率
	RECORD_SECONDS = 5  # 录音时间
	WAVE_OUTPUT_FILENAME = "1.wav"  # 录音后存储文件名
	p = pyaudio.PyAudio() # pyaudio实例化，初始化
	# 打开数据流，开始录音
	stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=CHUNK)
	print("开始录音,请说话......")
	frames = []
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK) #一次性录音采样字节大小
		frames.append(data)
	print("录音结束")
	# 停止数据流，停止录音
	stream.stop_stream()
	stream.close()
	p.terminate()  # 关闭pyaudio
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')  # 将录制的音频内容写入wav音频文件
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT)) # 处理采样的量化格式
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))  # b为空字符
	wf.close()
	# 识别本地文件，调用百度语音识别api
	a = client.asr(get_file_content('1.wav'), 'pcm', 16000, {
		'dev_pid': 1536,
	})
	return a['result'][0]





