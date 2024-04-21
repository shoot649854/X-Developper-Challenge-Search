import { HiMagnifyingGlass } from 'react-icons/hi2';
import React, { useState } from 'react';
import { Button } from '@mui/material';
import { useRouter } from 'next/router';

const Search = () => {
	const router = useRouter(); // Hook to access the router object

	const [searchQuery, setSearchQuery] = useState('');

    const handleInputChange = (event: any) => {
        setSearchQuery(event.target.value); // Update the search query state
    };

    const handleButtonClick = () => {
        // Navigate to the /api route, potentially with the search query as a query parameter
        // Adjust the path as needed, e.g., if you want to include the search query in the navigation
        router.push(`/search/${searchQuery}`);
    };

    const handleKeyPress = (event: any) => {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent the form from submitting traditionally
            handleButtonClick(); // Reuse the button click handler for Enter key press
        }
    };

	return (
	<div className="sticky top-0 bg-white py-2 mb-3">
		<form className="flex flex-col flex-1 gap-y-4">
			<div className="flex flex-1 relative">
				<HiMagnifyingGlass className="w-5 h-5 left-2.5 top-2 absolute flex items-center" />
				<input
					type="search"
					placeholder="Search"
					className="w-full flex items-center pl-10 pr-4 text-sm placeholder:text-sm placeholder:font-medium py-2 bg-slate-100 border-slate-100 placeholder:text-slate-700 rounded-full"
					onChange={handleInputChange}
				/>
				<Button
					variant="contained"
					color="primary"
					className="ml-2"
					disableElevation
					onClick={handleButtonClick}
					onKeyPress={handleKeyPress}
				>
					Tweet
				</Button>
			</div>
		</form>
	</div>
);
}

export default Search;
