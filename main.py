import tkinter as tk
import threading
import time
import random

def bubble_sort_animation(canvas, array, stop_event, label, timer_label):
    start_time = time.time()
    n = len(array)
    for i in range(n):
        for j in range(0, n-i-1):
            if stop_event.is_set():
                return
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
                draw_bars(canvas, array)
                elapsed_time = time.time() - start_time
                timer_label.config(text=f"Elapsed Time: {elapsed_time:.2f} s")
                time.sleep(0.1)
    label.config(text="Bubble Sort - Sorted")

def bogosort_animation(canvas, array, stop_event, label, timer_label):
    start_time = time.time()
    while not is_sorted(array):
        if stop_event.is_set():
            return
        random.shuffle(array)
        draw_bars(canvas, array)
        elapsed_time = time.time() - start_time
        timer_label.config(text=f"Elapsed Time: {elapsed_time:.2f} s")
        time.sleep(0.1)
    label.config(text="Bogosort - Sorted")

def merge_sort_animation(canvas, array, stop_event, label, timer_label):
    start_time = time.time()
    merge_sort_recursive(canvas, array, 0, len(array)-1, stop_event, label, timer_label, start_time)
    elapsed_time = time.time() - start_time
    timer_label.config(text=f"Elapsed Time: {elapsed_time:.2f} s")
    label.config(text="Merge sort - Sorted")

def merge_sort_recursive(canvas, array, left, right, stop_event, label, timer_label, start_time):
    if left < right:
        middle = (left + right) // 2
        merge_sort_recursive(canvas, array, left, middle, stop_event, label, timer_label, start_time)
        merge_sort_recursive(canvas, array, middle + 1, right, stop_event, label, timer_label, start_time)
        merge(canvas, array, left, middle, right, stop_event, label, timer_label, start_time)

def merge(canvas, array, left, middle, right, stop_event, label, timer_label, start_time):
    if stop_event.is_set():
        return
    left_array = array[left:middle + 1]
    right_array = array[middle + 1:right + 1]

    i = j = 0
    k = left

    while i < len(left_array) and j < len(right_array):
        if left_array[i] <= right_array[j]:
            array[k] = left_array[i]
            i += 1
        else:
            array[k] = right_array[j]
            j += 1
        k += 1
        draw_bars(canvas, array)
        elapsed_time = time.time() - start_time
        timer_label.config(text=f"Elapsed Time: {elapsed_time:.2f} s")
        time.sleep(0.1)

    while i < len(left_array):
        array[k] = left_array[i]
        i += 1
        k += 1
        draw_bars(canvas, array)
        elapsed_time = time.time() - start_time
        timer_label.config(text=f"Elapsed Time: {elapsed_time:.2f} s")
        time.sleep(0.1)

    while j < len(right_array):
        array[k] = right_array[j]
        j += 1
        k += 1
        draw_bars(canvas, array)
        elapsed_time = time.time() - start_time
        timer_label.config(text=f"Elapsed Time: {elapsed_time:.2f} s")
        time.sleep(0.1)

def is_sorted(array):
    return all(array[i] <= array[i+1] for i in range(len(array)-1))

def draw_bars(canvas, array):
    canvas.delete("all")
    canvas_height = canvas.winfo_height()
    canvas_width = canvas.winfo_width()
    bar_width = canvas_width / len(array)
    for i, value in enumerate(array):
        x1 = i * bar_width
        y1 = canvas_height - value
        x2 = (i + 1) * bar_width
        y2 = canvas_height
        canvas.create_rectangle(x1, y1, x2, y2, fill="blue")

def start_sorting():
    button_start['state'] = 'disabled'
    button_stop['state'] = 'normal'
    button_restart['state'] = 'normal'
    stop_event.clear()
    # Pornim firele de execuție pentru sortare
    global bubble_thread, bogosort_thread, merge_sort_thread
    bubble_thread = threading.Thread(target=bubble_sort_animation,
                                     args=(canvas1, array.copy(), stop_event, label1, timer_label1))
    bogosort_thread = threading.Thread(target=bogosort_animation,
                                       args=(canvas2, array.copy(), stop_event, label2, timer_label2))
    merge_sort_thread = threading.Thread(target=merge_sort_animation,
                                         args=(canvas3, array.copy(), stop_event, label3, timer_label3))
    bubble_thread.start()
    bogosort_thread.start()
    merge_sort_thread.start()

def stop_sorting():
    stop_event.set()
    button_start['state'] = 'normal'
    button_stop['state'] = 'disabled'

def restart_sorting():
    global array
    array = [random.randint(10, 200) for _ in range(10)]
    draw_bars(canvas1, array)
    draw_bars(canvas2, array)
    draw_bars(canvas3, array)
    label1.config(text="Bubble Sort")
    label2.config(text="Bogosort")
    label3.config(text="Merge Sort")
    timer_label1.config(text="Elapsed Time: 0.00 s")
    timer_label2.config(text="Elapsed Time: 0.00 s")
    timer_label3.config(text="Elapsed Time: 0.00 s")
    start_sorting()
    array_label.config(text=f"Array: {array}")

# Crearea ferestrei principale
root = tk.Tk()
root.title("Animatie sortare")

# Generare array aleator
array = [random.randint(10, 200) for _ in range(10)]

# Crearea primului canvas pentru bubble sort
canvas1 = tk.Canvas(root, height=200, width=400, bg="white")
canvas1.pack(side=tk.LEFT, padx=10)

# Crearea celui de-al doilea canvas pentru bogosort
canvas2 = tk.Canvas(root, height=200, width=400, bg="white")
canvas2.pack(side=tk.LEFT, padx=10)

# Crearea celui de-al treilea canvas pentru merge sort
canvas3 = tk.Canvas(root, height=200, width=400, bg="white")
canvas3.pack(side=tk.LEFT, padx=10)

array_label = tk.Label(root, text=f"Array: {array}")
array_label.pack(side=tk.TOP, pady=5)

# Etichete pentru a indica tipul de sortare și array-ul
label1 = tk.Label(root, text="Bubble Sort")
label1.pack(side=tk.TOP, pady=5)
timer_label1 = tk.Label(root, text="Elapsed Time: 0.00 s")
timer_label1.pack(side=tk.TOP, pady=5)

label2 = tk.Label(root, text="Bogosort")
label2.pack(side=tk.TOP, pady=5)
timer_label2 = tk.Label(root, text="Elapsed Time: 0.00 s")
timer_label2.pack(side=tk.TOP, pady=5)

label3 = tk.Label(root, text="Merge Sort")
label3.pack(side=tk.TOP, pady=5)
timer_label3 = tk.Label(root, text="Elapsed Time: 0.00 s")
timer_label3.pack(side=tk.TOP, pady=5)

# Crearea butoanelor și a firelor pentru sortare
button_start = tk.Button(root, text="Start Sorting", command=start_sorting)
button_start.pack(side=tk.TOP, pady=10)

button_stop = tk.Button(root, text="Stop Sorting", command=stop_sorting, state='disabled')
button_stop.pack(side=tk.TOP, pady=10)

button_restart = tk.Button(root, text="Restart", command=restart_sorting, state='disabled')
button_restart.pack(side=tk.TOP, pady=10)

# Eveniment pentru oprirea animațiilor
stop_event = threading.Event()

# Rularea buclei principale
root.mainloop()
