from deepface import DeepFace

# result = DeepFace.verify(img1_path="D:/project/facecheck/rishabh.jpeg", img2_path="D:/project/facecheck/RishabhVyas.png")
# result = DeepFace.verify(img1_path="https://res.cloudinary.com/dyoqttxkp/image/upload/v1744620301/WorkEase/file_tkcjbs.jpg", img2_path="https://res.cloudinary.com/dyoqttxkp/image/upload/v1744623899/harshanand_1_zncyhk.jpg")
result = DeepFace.verify(img1_path="https://res.cloudinary.com/dyoqttxkp/image/upload/v1744620301/WorkEase/file_tkcjbs.jpg", img2_path="https://res.cloudinary.com/dyoqttxkp/image/upload/v1744620301/WorkEase/file_tkcjbs.jpg")

print("Is Same Person:", result["verified"])
