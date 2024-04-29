import { useState, useEffect } from "react";
import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import Slider from "@mui/material/Slider";
import MuiInput from "@mui/material/Input";
import BlurOnIcon from "@mui/icons-material/BlurOn";

const Input = styled(MuiInput)`
	width: 42px;
`;

const BlurSelector = ({ setImgBlurLevel }) => {
	const [value, setValue] = useState(1);

	const handleSliderChange = (event, newValue) => {
		setValue(newValue);
	};

	const handleInputChange = (event) => {
		setValue(event.target.value === "" ? 0 : Number(event.target.value));
	};

	const handleBlur = () => {
		if (value < 0) {
			setValue(0);
		} else if (value > 5) {
			setValue(5);
		}
	};

	useEffect(() => {
		setImgBlurLevel(value);
	}, [value, setImgBlurLevel]);

	return (
		<Box sx={{ width: 250 }}>
			<Typography id="input-slider" variant="h6" gutterBottom>
				Blur Level
			</Typography>
			<Grid container spacing={2} alignItems="center">
				<Grid item>
					<BlurOnIcon />
				</Grid>
				<Grid item xs>
					<Slider
						aria-labelledby="input-slider"
						aria-label="Blur Level"
						value={typeof value === "number" ? value : 1}
						valueLabelDisplay="auto"
						// shiftStep={1}
						step={1}
						marks={true}
						min={1}
						max={5}
						onChange={handleSliderChange}
					/>
				</Grid>
				<Grid item>
					<Input
						value={value}
						size="small"
						onChange={handleInputChange}
						onBlur={handleBlur}
						inputProps={{
							step: 1,
							min: 1,
							max: 5,
							type: "number",
							"aria-labelledby": "input-slider",
						}}
					/>
				</Grid>
			</Grid>
		</Box>
	);
};

export default BlurSelector;
