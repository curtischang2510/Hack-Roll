class OpenCV:
    def __init__(self):
        self.cap = cv2.VideoCapture(1) # Use 0 for default camera. 1 if you have iPhone with continuity
        self.face_detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        
        self.model_points = np.array([
            (0.0, 0.0, 0.0),             # Nose tip
            (0.0, -330.0, -65.0),        # Chin
            (-225.0, 170.0, -135.0),     # Left eye left corner
            (225.0, 170.0, -135.0),      # Right eye right corner
            (-150.0, -150.0, -125.0),    # Left Mouth corner
            (150.0, -150.0, -125.0)      # Right mouth corner
        ], dtype=np.float64)

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def run(self):
        if not self.cap.isOpened():
            print("Cannot open camera")
            exit()

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Can't receive frame. Exiting ...")
                break

            processed_frame = self.draw_frame(frame)

            cv2.imshow('Webcam', processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()