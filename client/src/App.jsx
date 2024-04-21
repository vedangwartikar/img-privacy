import { useState } from "react";
import axios from "axios";

function App() {
	const [selectedFile, setSelectedFile] = useState(null);
	const [blurLevel, setBlurLevel] = useState(1);
	const [processedImage, setProcessedImage] = useState(null);

	const handleFileChange = (event) => {
		setSelectedFile(event.target.files[0]);
	};

	const handleUpload = async () => {
		if (!selectedFile) {
			alert("Please select an image");
			return;
		}

		const formData = new FormData();
		formData.append("image", selectedFile);
		formData.append("blur_level", blurLevel);

		try {
			const response = await axios.post(
				"http://127.0.0.1:5000/blur_sensitive_info",
				formData,
				{
					headers: {
						"Content-Type": "multipart/form-data",
					},
				}
			);
			console.log("\nresponse:", response.data);
			// setProcessedImage(URL.createObjectURL(response.data));
			setProcessedImage(
				`data:image/jpeg;base64,${response.data.blurred_image}`
			);
		} catch (error) {
			console.log("\nERROR>> ", error);
			// alert("Error uploading image. Please try again.");
		}
	};

	const handleBlurLevelChange = (e) => {
		setBlurLevel(parseInt(e.target.value));
	};

	return (
		<div>
			<h1>Image Privacy Protection</h1>
			<input type="file" accept="image/*" onChange={handleFileChange} />
			<br />
			<br />
			<label htmlFor="Blur Level">Blur Level</label>{" "}
			<select value={blurLevel} onChange={handleBlurLevelChange}>
				<option value={1}>Level 1</option>
				<option value={2}>Level 2</option>
				<option value={3}>Level 3</option>
				<option value={4}>Level 4</option>
				<option value={5}>Level 5</option>
			</select>
			<br />
			<br />
			<button onClick={handleUpload}>Upload Image</button>
			<br />
			{processedImage && (
				<div>
					<h2>Processed Image</h2>
					<img
						src={processedImage}
						alt="Processed"
						style={{ maxWidth: "50%" }}
					/>
				</div>
			)}
		</div>
	);
}

export default App;
