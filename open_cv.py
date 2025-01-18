import cv2
import dlib
import numpy as np



class OpenCV:
    def __init__(self, callback=None):
        self.cap = cv2.VideoCapture(1)  # Use 0 for default camera, 1 for external camera
        
        if not self.cap.isOpened():
            print("Camera index 1 failed. Trying index 0...")
            self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            print("Failed to open camera at both index 1 and 0.")
            raise RuntimeError("Cannot access camera.")
        
        self.face_detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.callback = callback  # Callback to pass frames to GUI
        self.running = True  # Control flag for stopping the thread

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

    def process_frame(self):
        """Process a single frame and pass it to the callback."""
        if not self.cap.isOpened():
            print("Cannot open camera")
            return None

        ret, frame = self.cap.read()
        if not ret:
            print("Can't receive frame.")
            return None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector(gray)

        user_is_looking = False

        for face in faces:
            landmarks = self.predictor(gray, face)

            # Check head pose and eye tracking
            head_pose_check = self.is_user_looking_at_screen(frame, landmarks)
            eye_tracking_check = self.eye_tracking(gray, frame, landmarks)

            # Draw facial landmarks
            for i in range(68):
                x = landmarks.part(i).x
                y = landmarks.part(i).y
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # Draw bounding box
            cv2.rectangle(
                frame, 
                (face.left(), face.top()), 
                (face.right(), face.bottom()), 
                (255, 0, 0), 2
            )

            # Combine both checks
            user_is_looking = head_pose_check and eye_tracking_check
            
            print(f"Head pose: {head_pose_check}, Eye tracking: {eye_tracking_check} \n User is looking: {user_is_looking}")

            if not user_is_looking:
                # Add a red overlay if the user is not looking
                red_overlay = np.full(frame.shape, (0, 0, 255), dtype=np.uint8)
                cv2.addWeighted(red_overlay, 0.5, frame, 0.5, 0, frame)

        if len(faces) == 0:
            # Add red overlay if no faces are detected
            red_overlay = np.full(frame.shape, (0, 0, 255), dtype=np.uint8)
            cv2.addWeighted(red_overlay, 0.5, frame, 0.5, 0, frame)
            user_is_looking = False

        # Trigger callback to pass the processed frame to the GUI
        if self.callback:
            self.callback(user_is_looking, frame)

        return frame

    def run(self):
        """Continuously process frames."""
        while self.running:
            self.process_frame()

    def stop(self):
        """Stop capturing frames."""
        self.running = False

    def is_user_looking_at_screen(self, frame, landmarks):
        size = frame.shape
        focal_length = size[1]
        center = (size[1] / 2, size[0] / 2)
        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype="double")
        dist_coeffs = np.zeros((4, 1)) 

        image_points = np.array([
            (landmarks.part(30).x, landmarks.part(30).y),  # Nose tip
            (landmarks.part(8).x, landmarks.part(8).y),    # Chin
            (landmarks.part(36).x, landmarks.part(36).y),  # Left eye left corner
            (landmarks.part(45).x, landmarks.part(45).y),  # Right eye right corner
            (landmarks.part(48).x, landmarks.part(48).y),  # Left Mouth corner
            (landmarks.part(54).x, landmarks.part(54).y)   # Right mouth corner
        ], dtype="double")

        success, rotation_vector, translation_vector = cv2.solvePnP(
            self.model_points, 
            image_points, 
            camera_matrix, 
            dist_coeffs, 
            flags=cv2.SOLVEPNP_ITERATIVE
        )

        if not success:
            print("Pose estimation failed")
            return False

        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
        proj_matrix = np.hstack((rotation_matrix, translation_vector))
        _, _, _, _, _, _, euler_angles = cv2.decomposeProjectionMatrix(proj_matrix)

        yaw = euler_angles[1, 0]
        pitch = euler_angles[0, 0]


        yaw_threshold = 30
        pitch_threshold = 160

        print(f"Yaw: {abs(yaw)}, Pitch: {abs(pitch)}")

        if abs(yaw) > yaw_threshold or abs(pitch) < pitch_threshold:
            return False
        else:
            return True

    def eye_tracking(self, gray, frame, landmarks):
        def get_eye_region(landmarks, start, end):
            points = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(start, end + 1)]
            region = np.array(points, dtype=np.int32)
            return region

        def crop_eye(frame, region):
            mask = np.zeros_like(frame)
            cv2.fillPoly(mask, [region], (255, 255, 255))
            eye = cv2.bitwise_and(frame, mask)
            x, y, w, h = cv2.boundingRect(region)
            eye = eye[y:y + h, x:x + w]
            return eye, x, y
        
        # Get eye regions
        left_eye_region = get_eye_region(landmarks, 36, 41)
        right_eye_region = get_eye_region(landmarks, 42, 47)

        left_eye, left_x, left_y = crop_eye(gray, left_eye_region)
        right_eye, right_x, right_y = crop_eye(gray, right_eye_region)

        def detect_pupil(eye):
            _, thresh = cv2.threshold(eye, 70, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                max_contour = max(contours, key=cv2.contourArea)
                (cx, cy), radius = cv2.minEnclosingCircle(max_contour)
                if radius > 0:
                    return int(cx), int(cy)
            return None

        left_pupil = detect_pupil(left_eye)
        right_pupil = detect_pupil(right_eye)

        if left_pupil and right_pupil:
            left_pupil_global = (left_pupil[0] + left_x, left_pupil[1] + left_y)
            right_pupil_global = (right_pupil[0] + right_x, right_pupil[1] + right_y)

            cv2.circle(frame, left_pupil_global, 3, (0, 0, 255), -1)
            cv2.circle(frame, right_pupil_global, 3, (0, 0, 255), -1)


            left_eye_center = np.mean(left_eye_region, axis=0)
            right_eye_center = np.mean(right_eye_region, axis=0)
            screen_gaze = abs(left_pupil_global[0] - left_eye_center[0]) < 15 and \
                        abs(right_pupil_global[0] - right_eye_center[0]) < 15
            return screen_gaze
        return False


