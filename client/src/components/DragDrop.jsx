import { useEffect, useState } from "react";
import InputLabel from "@mui/material/InputLabel";
import { AiOutlineCheckCircle, AiOutlineCloudUpload } from "react-icons/ai";
import { MdClear } from "react-icons/md";

import "../styles/drag-drop.scss";

const DragDrop = ({ onFilesSelected, width, height }) => {
	const [files, setFiles] = useState([]);

	const fileChangeHandler = (event) => {
		const selectedFiles = event.target.files;

		if (selectedFiles && selectedFiles.length > 0) {
			const newFiles = Array.from(selectedFiles);
			setFiles((prevFiles) => [...prevFiles, ...newFiles]);
		}
	};

	const onDropHandler = (event) => {
		event.preventDefault();

		const droppedFiles = event.dataTransfer.files;

		if (droppedFiles.length > 0) {
			const newFiles = Array.from(droppedFiles);
			setFiles((prevFiles) => [...prevFiles, ...newFiles]);
		}
	};

	const onFileRemoveHandler = (index) => {
		setFiles((prevFiles) => prevFiles.filter((_, i) => i !== index));
	};

	useEffect(() => {
		onFilesSelected(files);
	}, [files, onFilesSelected]);

	return (
		<div
			className="drag-drop-section"
			style={{ width: width, height: height }}
		>
			<div
				className={`document-uploader ${
					files.length > 0 ? "upload-box active" : "upload-box"
				}`}
				onDrop={onDropHandler}
				onDragOver={(e) => e.preventDefault()}
			>
				<>
					<div className="upload-info">
						<AiOutlineCloudUpload />

						<div>
							<p>Drag and drop your file here</p>
							<p className="sub-text">
								Supported files: .PNG, .JPG, .JPEG
							</p>
						</div>
					</div>

					<input
						id="browse"
						type="file"
						accept=".png,.jpg,.jpeg"
						multiple={false}
						hidden={true}
						onChange={fileChangeHandler}
					/>

					<InputLabel htmlFor="browse" className="browse-btn">
						or click to browse file
					</InputLabel>
				</>

				{files.length > 0 && (
					<div className="file-list">
						<div className="file-list__container">
							{files.map((file, index) => (
								<div className="file-item" key={index}>
									<div className="file-info">
										<p>{file.name}</p>
									</div>

									<div className="file-actions">
										<MdClear
											onClick={() =>
												onFileRemoveHandler(index)
											}
										/>
									</div>
								</div>
							))}
						</div>
					</div>
				)}

				{files.length > 0 && (
					<div className="success-file">
						<AiOutlineCheckCircle
							style={{ color: "#6DC24B", marginRight: 1 }}
						/>

						<p>{files.length} file(s) selected</p>
					</div>
				)}
			</div>
		</div>
	);
};

export default DragDrop;
