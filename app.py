import cv2
import dbr
import time
import os
from multiprocessing import Process, Queue, Condition, Value, Array
from pylgbst import get_connection_auto
from pylgbst.hub import MoveHub

class Result:
    def __init__(self, image, results):
        self.image = image
        self.results = results

def dbr_run(frame_queue, key_queue, cond, num, result_queue):
    conn = get_connection_auto()  
    try:
        hub = MoveHub(conn)
        print('Robot connected')
        speed = 0.5
        dbr.initLicense('t0126lQMAAJKX0RvMyzlh6PuQjcJyenARHjo4+sFqhwweCXfp3hAVHYasqSvCLpym3urmWpADdzSI19PIjSv4RBLR1HkSjR7O0lsOF8wumF0wu2B2wRyCOQRzCOYQzCGYKZgpmCmYKZjzW+sncrPQMG8MWRNv9W/aWNJhfgMslLDp')
        while num.value == 1:
            print('wait for event')
            key = key_queue.get()
            if key == ord('q'):
                break

            try:
                if key == ord('c'):
                    inputframe = frame_queue.get()
                    results = dbr.decodeBuffer(inputframe, 0x4000000)
                    if (len(results) > 0):
                        print(get_time())
                        print("Total count: " + str(len(results)))
                        for result in results:
                            print("Type: " + result[0])
                            print("Value: " + result[1] + "\n")

                        result_queue.put(Result(inputframe, results))

                elif key == ord('a'):
                    # left
                    print('left')
                    hub.motor_AB.angled(90, speed * -1, speed)
                elif key == ord('d'):
                    # right
                    print('right')
                    hub.motor_AB.angled(90, speed, speed * -1)
                elif key == ord('w'):
                    # up
                    print('up')
                    
                    hub.motor_AB.constant(speed)
                elif key == ord('s'):
                    # down
                    print('down')
                    hub.motor_AB.constant(speed * -1)
                elif key == ord('p'):
                    print('pause')
                    hub.motor_AB.stop(is_async=True)
            except:
                pass

        dbr.destroy()
        print("Detection is done.")

    finally:
        conn.disconnect()


def get_time():
    localtime = time.localtime()
    capturetime = time.strftime("%Y%m%d%H%M%S", localtime)
    return capturetime


def read_barcode():
    num = Value('i', 1)
    result_queue = Queue(1)
    key_queue = Queue(1)
    frame_queue = Queue(1)
    cond = Condition()
    dbr_proc = Process(target=dbr_run, args=(
        frame_queue, key_queue, cond, num, result_queue))
    dbr_proc.start()

    vc = cv2.VideoCapture(0)
    vc.set(3, 640) #set width
    vc.set(4, 480) #set height

    if vc.isOpened():  # try to get the first frame
        rval, frame = vc.read()
    else:
        return

    windowName = "Robot View"
    
    try:
        while True:
            rval, frame = vc.read()
            cv2.imshow(windowName, frame)

            key = cv2.waitKey(1) & 0xFF 
            if key == ord('q'):
                key_queue.put(key)
                dbr_proc.join()
                break
            elif key == ord('c'):
                frame_queue.put(frame)
                key_queue.put(key)
            elif key == ord('a') or key == ord('d') or key == ord('w') or key == ord('s') or key == ord('p'):
                key_queue.put(key)

            try:
                ret = result_queue.get_nowait()
                results = ret.results
                image = ret.image

                thickness = 2
                color = (0,255,0)
                for result in results:
                    print("barcode format: " + result[0])
                    print("barcode value: " + result[1])
                    x1 = result[2]
                    y1 = result[3]
                    x2 = result[4]
                    y2 = result[5]
                    x3 = result[6]
                    y3 = result[7]
                    x4 = result[8]
                    y4 = result[9]

                    cv2.line(image, (x1, y1), (x2, y2), color, thickness)
                    cv2.line(image, (x2, y2), (x3, y3), color, thickness)
                    cv2.line(image, (x3, y3), (x4, y4), color, thickness)
                    cv2.line(image, (x4, y4), (x1, y1), color, thickness)

                    cv2.putText(image, result[1], (min([x1, x2, x3, x4]), min([y1, y2, y3, y4])), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), thickness)

                cv2.imshow("Localization", image)


            except:
                pass
    finally:
        num.value = 0
        
            
    vc.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("OpenCV version: " + cv2.__version__)
    read_barcode()
