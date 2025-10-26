# Libraries Import
import re
import tkinter as tk
from collections import namedtuple

BUTTON = ['C', 'BIN', 'DEC', 'HEX', 'CUT']

# 電卓

class Convert():
	#-------------------------------------------
	# 16進数に変換可能か検証する
	#-------------------------------------------
	def is_hex_dec_bin(self, val, base):
		try:
			int(val, base)
			return True
		except ValueError:
			return False

	#-------------------------------------------
	# 2進/10進/16進判定
	#-------------------------------------------
	def judge_hex_dec_bin(self, code):
		if code.startswith('0b') == True:
			# 2進数
			return 2
		elif (code.startswith('0x') == True) or\
			 (re.search(r'[a-f]', code, re.IGNORECASE)):
			# 16進数
			return 16
		else:
			# 10進数
			return 10

	#-------------------------------------------
	# 2進数に変換
	#-------------------------------------------
	def binary(self, code):
		#2進/10進/16進判定
		base = self.judge_hex_dec_bin(code)

		# 2進数に変換
		ret = self.is_hex_dec_bin(code, base)
		return ret, (bin(int(code, base)) if ret == True else "")

	#-------------------------------------------
	# 10進数に変換
	#-------------------------------------------
	def decimal(self, code):
		#2進/10進/16進判定
		base = self.judge_hex_dec_bin(code)

		# 10進数に変換
		ret = self.is_hex_dec_bin(code, base)
		return ret, (int(code, base) if ret == True else "")

	#-------------------------------------------
	# 16進数に変換
	#-------------------------------------------
	def hex(self, code):
		#2進/10進/16進判定
		base = self.judge_hex_dec_bin(code)

		# 10進数に変換
		ret = self.is_hex_dec_bin(code, base)
		if ret == True:
			hex_uppercase = hex(int(code, base)).upper()
			hex_uppercase = hex_uppercase.replace('X', 'x')
			return True, hex_uppercase
		else:
			return False, ""

#-------------------------------------------
# 履歴1～3が選択されたときの処理
#-------------------------------------------
def select_history(event):
	code = event.widget['text']
	i = code.find('=')
	entry_var.set(code[:i] if i != -1 else code)

#-------------------------------------------
# 表示の初期化
#-------------------------------------------
def clear(event):
	entry_var.set("")
	info_var.set("")
	history_var[0].set('')
	history_var[1].set('')
	history_var[2].set('')

#-------------------------------------------
# 式が実行可能か検証する
#-------------------------------------------
def is_eval_excutable(code):
	try:
		result = eval(code)
		return True
	except Exception as e:
		return False

#-------------------------------------------
# 式でEnterキーが押されたときの処理
#-------------------------------------------
def click_calc(event):
	# メッセージクリア
	info_var.set("")

	# 式を取得
	code = entry_var.get()

	# 式が実行可能か検証
	if is_eval_excutable(code) != True:
		info_var.set("Calculation formula that cannot be executed")
		return

	# eval()を実行
	result = eval(code)

	# 式が前回と違うときのみ履歴を更新する
	if history_var[0].get() != code+"="+str(result):
		history_var[2].set(history_var[1].get())
		history_var[1].set(history_var[0].get())
		history_var[0].set(code+"="+str(result))
		entry_var.set(str(result))
		entry.icursor(tk.END)

#-------------------------------------------
# 小数点以下を切り捨て
#-------------------------------------------
def cut_point(event):
	s = entry_var.get().split('.')[0]
	entry_var.set(s)

#-------------------------------------------
# 機能ボタンが押されたときの処理
#-------------------------------------------
def func_button(event):
	check = event.widget['text']

	if check == 'C':
		# Clear
		clear(event)

	elif check == 'BIN':
		# 2進数に変換
		ret, result = Convert().binary(entry_var.get())
		entry_var.set(result) if ret == True else info_var.set("cannot convert")

	elif check == 'DEC':
		# 10進数に変換
		ret, result = Convert().decimal(entry_var.get())
		entry_var.set(result) if ret == True else info_var.set("cannot convert")

	elif check == 'HEX':
		# 16進数に変換
		ret, result = Convert().hex(entry_var.get())
		entry_var.set(result) if ret == True else info_var.set("cannot convert")

	elif check == 'CUT':
		# 小数点以下を切り捨て
		cut_point(event)

#-------------------------------------------
# ショートカットキーが押されたときの処理
#-------------------------------------------
def keypress_convert(check):
	if check == 'BIN':
		# 2進数に変換
		ret, result = Convert().binary(entry_var.get())
		entry_var.set(result) if ret == True else info_var.set("cannot convert")

	elif check == 'DEC':
		# 10進数に変換
		ret, result = Convert().decimal(entry_var.get())
		entry_var.set(result) if ret == True else info_var.set("cannot convert")

	elif check == 'HEX':
		# 16進数に変換
		ret, result = Convert().hex(entry_var.get())
		entry_var.set(result) if ret == True else info_var.set("cannot convert")

################################################################################
#-------------------------------------------
# define
#-------------------------------------------
BG_COLOR = 'lightslategray'
FG_COLOR = 'linen'

#-------------------------------------------
# window setting
#-------------------------------------------
root = tk.Tk()
root.resizable(width=False, height=False)
root.title(u"電卓")	# Windowのタイトル
root.geometry("500x300") # Windowサイズ
root.configure(bg=BG_COLOR)
root.update_idletasks() # 設定値の更新

#-------------------------------------------
# ESCキー押下で式、履歴をクリア
#-------------------------------------------
label = tk.Label(root, text="", fg=FG_COLOR, bg=BG_COLOR)
label.pack()
root.bind('<Escape>', clear)

#-------------------------------------------
# 3世代の計算式の配置
#-------------------------------------------
# Frame設定
calc_frame = tk.Frame(root, width=root.winfo_width() - 40, height=170, bg=BG_COLOR)
calc_frame.propagate(False) # サイズを固定
calc_frame.place(x=20, y=20) # フレームの配置位置

# 履歴の動的変数
history_var = [tk.StringVar(), tk.StringVar(), tk.StringVar()]

# 式の配置
for i in reversed(range(0, 3)):
	history = tk.Label(calc_frame, textvariable=history_var[i], font=("Lucida Console",14), fg=FG_COLOR, bg=BG_COLOR)
	history.pack(pady=5, anchor='e')
	history.bind('<Button-1>', select_history)

#-------------------------------------------
# 計算式
#-------------------------------------------
# 計算式用の動的変数
entry_var = tk.StringVar()

# 式の配置
entry = tk.Entry(calc_frame, textvariable=entry_var, font=("",35), justify=tk.RIGHT,\
				width=root.winfo_width()-40, relief=tk.GROOVE, fg=FG_COLOR, bg=BG_COLOR)
entry.pack(pady=5)

# フォーカスを設定
entry.focus_set()

# Enterが押された場合
entry.bind('<Return>', click_calc)

#-------------------------------------------
# ボタン設定
#-------------------------------------------
# Frame設定
button_frame = tk.Frame(root, width=root.winfo_width(), height=20, bg=BG_COLOR)
button_frame.propagate(False) # サイズを固定
button_frame.place(x=20, y=200) # フレームの配置位置

# ボタンの配置
for i, name in enumerate(BUTTON): # Buttonの配置
	button = tk.Button(button_frame, text=name, font=('', 12), width=4, height=2,\
						relief=tk.GROOVE, fg=FG_COLOR, bg=BG_COLOR)
	button.grid(row=1, column=i) # 列や行を指定して配置

	# Buttonが押された場合
	button.bind('<Button-1>', func_button)

	# ショートカットキーが押された場合
	root.bind("<Alt-KeyPress-c>", clear)
	root.bind("<Alt-KeyPress-b>", lambda event: keypress_convert("BIN"))
	root.bind("<Alt-KeyPress-d>", lambda event: keypress_convert("DEC"))
	root.bind("<Alt-KeyPress-h>", lambda event: keypress_convert("HEX"))
	root.bind("<Alt-KeyPress-p>", cut_point)

#-------------------------------------------
# メッセージ
#-------------------------------------------
# Frame設定
info_frame = tk.Frame(root, width=root.winfo_width() - 40, height=40, bg=BG_COLOR)
info_frame.propagate(False) # サイズを固定
info_frame.place(x=20, y=250) # フレームの配置位置

# メッセージ用の動的変数
info_var = tk.StringVar()

# メッセージの配置
info = tk.Label(info_frame, textvariable=info_var, font=("Lucida Console",12), fg=FG_COLOR, bg=BG_COLOR)
info.pack(pady=5, anchor='e')

# Display
root.mainloop()

#if __name__ == "__main__":
#	main()
