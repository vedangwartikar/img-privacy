import { useEffect, useState } from "react";
import axios from "axios";
import Button from "@mui/material/Button";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import DoneIcon from "@mui/icons-material/Done";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import Chip from "@mui/material/Chip";
import Stack from "@mui/material/Stack";
import LockResetIcon from "@mui/icons-material/LockReset";
import CloudDownloadIcon from "@mui/icons-material/CloudDownload";
import Switch from "@mui/material/Switch";
import LoadingButton from "@mui/lab/LoadingButton";

import DragDrop from "./components/DragDrop";
import BlurSelector from "./components/BlurSelector";

const App = () => {
	const [imgBlurLevel, setImgBlurLevel] = useState(1);
	const [vehicleDetected, setVehicleDetected] = useState(false);
	const [processedImage, setProcessedImage] = useState(null);
	const [uniqueObjects, setUniqueObjects] = useState(null);
	const [files, setFiles] = useState([]);
	const [checked, setChecked] = useState(false);
	const [loading, setLoading] = useState(false);
	const [selectedChips, setSelectedChips] = useState([]);

	const handleUpload = async (flag = "protect") => {
		if (files.length < 1) {
			alert("Please select an image");
			return;
		}

		const formData = new FormData();
		formData.append("image", files[0]);
		formData.append("blur_level", imgBlurLevel);
		formData.append("blur_license_plate", checked ? 1 : 0);
		formData.append("labels", selectedChips);

		try {
			setLoading(true);
			const response = await axios.post(
				"http://127.0.0.1:5000/blur_sensitive_info",
				formData,
				{
					headers: {
						"Content-Type": "multipart/form-data",
					},
				}
			);
			// console.log("\nresponse:", response.data);
			setProcessedImage(
				`data:image/jpeg;base64,${response.data.blurred_image}`
			);

			if (flag === "upload") {
				setUniqueObjects(response.data.unique_labels);
			}
		} catch (error) {
			console.log("\nERROR>> ", error);
			// alert("Error uploading image. Please try again.");
		}

		setLoading(false);
	};

	useEffect(() => {
		if (files.length > 0) {
			setUniqueObjects([]);
			setSelectedChips([]);
			setChecked(false);
		}
	}, [files]);

	useEffect(() => {
		if (uniqueObjects?.length > 0) {
			if (
				uniqueObjects.includes("car") ||
				uniqueObjects.includes("bus") ||
				uniqueObjects.includes("truck")
			) {
				setVehicleDetected(true);
			} else {
				setVehicleDetected(false);
			}
		}
	}, [uniqueObjects]);

	const handleChipClick = (chip) => {
		setSelectedChips((prevChips) => {
			if (prevChips.includes(chip)) {
				return prevChips.filter((c) => c !== chip);
			} else {
				return [...prevChips, chip];
			}
		});
	};

	const handleChange = (event) => {
		setChecked(event.target.checked);
	};

	return (
		<div className="app">
			<Typography variant="h3" gutterBottom>
				Image Privacy Protection
			</Typography>

			<DragDrop onFilesSelected={setFiles} width="300px" />

			<Button
				component="label"
				variant="contained"
				tabIndex={-1}
				startIcon={<CloudUploadIcon />}
				onClick={() => handleUpload("upload")}
			>
				Upload Image
			</Button>

			<Divider
				orientation="horizontal"
				variant="fullWidth"
				flexItem
				// style={{ marginTop: "60px" }}
			/>

			{processedImage && (
				<>
					<div className="parent-container">
						<div className="left-container">
							<Typography
								variant="h5"
								marginTop={5}
								marginBottom={2}
							>
								Your Image Preview
							</Typography>

							<div className="img-container">
								<img
									src={processedImage}
									alt="Processed"
									// style={{ maxWidth: "50%" }}
								/>
							</div>
						</div>

						<Divider
							orientation="vertical"
							variant="middle"
							flexItem
							style={{ marginTop: "60px" }}
						/>

						<div className="right-container">
							<Stack direction="row" spacing={1}>
								{uniqueObjects && (
									<>
										<div>
											<Typography
												variant="h6"
												// gutterBottom
												className="unique-objects-heading"
											>
												Objects Detected
											</Typography>

											<Typography
												variant="h6"
												// italic
												gutterBottom
												className="unique-objects-heading"
											>
												(select the objects you want to
												blur)
											</Typography>

											{uniqueObjects.map(
												(objectLabel, index) => (
													<Chip
														key={index}
														label={objectLabel}
														clickable={true}
														color="primary"
														onClick={() =>
															handleChipClick(
																objectLabel
															)
														}
														variant={
															selectedChips.includes(
																objectLabel
															)
																? "filled"
																: "outlined"
														}
														onDelete={() => {}}
														deleteIcon={
															selectedChips.includes(
																objectLabel
															) ? (
																<DoneIcon />
															) : (
																<></>
															)
														}
													/>
												)
											)}
										</div>
									</>
								)}
							</Stack>

							{vehicleDetected && (
								<>
									<div className="license-plate-toggle">
										<Typography
											variant="h6"
											gutterBottom
											style={{ margin: "0" }}
										>
											Blur License Plate of Vehicles
										</Typography>
										<Switch
											checked={checked}
											onChange={handleChange}
											inputProps={{
												"aria-label": "controlled",
											}}
										/>
									</div>
								</>
							)}

							<div className="blur-container">
								<BlurSelector
									setImgBlurLevel={setImgBlurLevel}
								/>
							</div>

							<div className="btn-container">
								<LoadingButton
									component="label"
									variant="contained"
									tabIndex={-1}
									loading={loading}
									loadingPosition="start"
									startIcon={<LockResetIcon />}
									onClick={() => handleUpload("protect")}
								>
									Protect my Image
								</LoadingButton>
							</div>
						</div>
					</div>

					<Divider
						orientation="horizontal"
						variant="fullWidth"
						flexItem
						style={{ marginTop: "30px" }}
					/>

					<div className="download-btn-container">
						<Button
							className="download-btn"
							component="label"
							variant="contained"
							tabIndex={-1}
							startIcon={<CloudDownloadIcon />}
						>
							<a href={processedImage} download>
								Download Image
							</a>
						</Button>
					</div>

					<Divider
						orientation="horizontal"
						variant="fullWidth"
						flexItem
						style={{ marginTop: "30px", marginBottom: "30px" }}
					/>
				</>
			)}
		</div>
	);
};

export default App;
