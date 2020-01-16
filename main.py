from summarizer import Summarizer
import tkinter as tk

def summarizeText():
    text = entry1.get("1.0",'end-1c')
    procent = int(entry2.get("1.0",'end-1c'))

    entry1.delete("1.0",tk.END);

    summarizer = Summarizer()
    nrSentences = summarizer.getNrSenteces(text)
    finalLength = int(procent/100 * nrSentences)
    if finalLength == 0:
        finalLength = 1
    result = summarizer.summarize(text)
    result = summarizer.sortSentences(result[:finalLength])
    result = [res['sentence'] for res in result]
    x2 = ""
    for el in result:
        x2 = x2 + el
    entry1.insert(tk.END,x2)

if __name__ == "__main__":
    # filename = "1.txt"
    # with open(filename) as f:
    #     text = f.read()
    # summarizer = Summarizer()
    # result = summarizer.summarize(text)
    # result = summarizer.sortSentences(result[:2])
    # result = [res['sentence'] for res in result]
    # print("Result: ")
    # for sentence in result:
    #     print(sentence)

    root = tk.Tk()

    canvas1 = tk.Canvas(root, width=800, height=600, relief='raised')
    canvas1.pack()

    label1 = tk.Label(root, text='The Summarizer')
    label1.config(font=('helvetica', 20))
    canvas1.create_window(400, 50, window=label1)

    label2 = tk.Label(root, text='Insert the text here:')
    label2.config(font=('helvetica', 10))
    canvas1.create_window(400, 135, window=label2)

    entry1 = tk.Text(root)
    canvas1.create_window(400, 350, window=entry1, height=400, width=750)

    label3 = tk.Label(root, text='Insert the rate here:')
    label3.config(font=('helvetica', 10))
    canvas1.create_window(400, 90, window=label3)

    entry2 = tk.Text(root)
    canvas1.create_window(400, 110, window=entry2, height=20, width=60)

    button1 = tk.Button(text='Text Summarizer', command=summarizeText, bg='brown', fg='white',
                        font=('helvetica', 9, 'bold'))
    canvas1.create_window(400, 580, window=button1)

    root.mainloop()