from open_cv import OpenCV

def callback(user_is_looking):
    print("Callback function:", user_is_looking)



if __name__ == "__main__":
    opencv = OpenCV(callback=callback)
    opencv.run()