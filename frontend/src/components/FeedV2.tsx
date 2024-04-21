import React, { useEffect, useState } from 'react';
import Image from 'next/image';
import Post from '@ui/Post';
import { ReactNode } from 'react';
import { Suspense } from 'react';
import { useRouter } from 'next/router';

interface PostItem {
	name: string;
	username: string;
	content: string;
	description: string;
	date: string;
	src: string;
	following: string;
	followers: string;
	initials: string;
	image?: ReactNode;
}

interface FeedProp {
	searchKeyword: string;
}

const FeedV2 = () => {
	const router = useRouter();
	const searchKeyword = router.query.slug as string; // Assuming 'slug' is the dynamic part of the path containing the search query
	const [posts, setPosts] = useState<PostItem[]>([]);
	const [loading, setLoading] = useState<boolean>(true);
	const [error, setError] = useState<string>('');
	const [description, setDescription] = useState<PostItem | null>(null);

	useEffect(() => {
		const fetchData = async () => {
			if (!searchKeyword) {
				return;
			}
			try {
				console.log(searchKeyword);
				const response = await fetch('http://127.0.0.1:4000/search', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
					},
					body: JSON.stringify({ query: searchKeyword }),
				});
				if (!response.ok) {
					throw new Error(`HTTP error! Status: ${response.status}`);
				}
				const data = await response.json();
				console.log(data)
				const parsedPosts = data[1].map((item) => item.tweet);
				setDescription(data[0]);
				console.log(parsedPosts);
				setPosts(parsedPosts);
			} catch (error: any) {
				setError(error.message);
				console.error('Error fetching data:', error);
			} finally {
				setLoading(false);
			}
		};

		fetchData();
	}, [searchKeyword]);

	if (loading) {
		return <Loading />;
	}

	if (error) {
		return <div>Error: {error}</div>;
	}
	return (
		<Suspense fallback={<Loading />}>
			<div className="bg-slate-100 p-4 rounded-lg shadow mb-4">
				<h2 className="text-lg font-semibold mb-2">Search Context</h2>
				<p className="text-slate-700">
					{description
						? description.description
						: 'No context available for this search.'}
				</p>
			</div>
			<ul className="[&_p:last-child]:text-slate-500 [&_p:first-child]:text-lg divide-y divide-slate-200">
				{posts.map((post, i) => (
					<li key={`post-${post.id}-${i}`} className="p-4">
						<Post
							name={post.name || 'John Doe'}
							username={post.username || 'elonmusk'}
							content={post.text || 'No content available'}
							date={
								new Date(post.created_at).toLocaleString() || 'Unknown date'
							}
							src={post.src || ''}
							initials={post.initials || ''}
							description={post.description || ''}
							followers={post.followers || '0'}
							following={post.following || '0'}
						>
							{post.image || ''}
						</Post>
					</li>
				))}
			</ul>
		</Suspense>
	);
};

export default FeedV2;

function Loading() {
	return <h2>Loading...</h2>;
}

// import React, { useEffect, useState } from 'react';
// import Image from 'next/image';
// import Post from '@ui/Post';
// import { ReactNode } from 'react';
// import { Suspense } from 'react';

// interface PostItem {
// 	name: string;
// 	username: string;
// 	content: string;
// 	description: string;
// 	date: string;
// 	src: string;
// 	following: string;
// 	followers: string;
// 	initials: string;
// 	image?: ReactNode;

// }

// const items: PostItem[] = [
// 	{
// 		name: 'Chinmay',
// 		username: 'ch1nmay',
// 		following: '249',
// 		followers: '663',
// 		content: 'Chinmay',
// 		description:
// 			'Improve your design skills by making projects. 1 every week, practice with me on Youtube. I use Figma, Tailwind CSS and Webflow.',
// 		date: '1h',
// 		src: 'https://images.unsplash.com/photo-1511485977113-f34c92461ad9?ixlib=rb-1.2.1&w=128&h=128&dpr=2&q=80',
// 		initials: 'JD',
// 		image: (
// 			<div className="w-full relative -z-10 h-80 mb-4">
// 				<Image
// 					fill={true}
// 					style={{ objectFit: 'cover' }}
// 					className="rounded-3xl"
// 					src="https://images.unsplash.com/photo-1635776062127-d379bfcba9f8?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2532&q=80"
// 					alt="Gradient"
// 				/>
// 			</div>
// 		),
// 	},
// 	{
// 		name: 'John Doe',
// 		username: 'johndoe',
// 		following: '138',
// 		followers: '2,218',
// 		content: 'I love Figma',
// 		description: 'I design and hug auto layout everyday',
// 		date: '2h',
// 		src: 'https://images.unsplash.com/photo-1532123675048-773bd75df1b4?ixlib=rb-1.2.1&w=128&h=128&dpr=2&q=80',
// 		initials: 'JD',
// 	},
// 	{
// 		name: 'Jessica Doe',
// 		username: 'jessicadoe',
// 		following: '866',
// 		followers: '1001',
// 		content: 'Tailwind CSS is insane',
// 		description:
// 			'Should designers code. Should you rename your Figma layers is the 1 billion…',
// 		date: '3h',
// 		src: 'https://images.unsplash.com/photo-1614644147798-f8c0fc9da7f6?ixlib=rb-1.2.1&w=128&h=128&dpr=2&q=80',
// 		initials: 'JD',
// 	},
// 	{
// 		name: 'Joe Doe',
// 		username: 'joedoe',
// 		following: '668',
// 		followers: '1985',
// 		content: 'Next JS documentation is so good',
// 		description: 'Next JS enthusiast',
// 		date: '4h',
// 		src: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-1.2.1&w=128&h=128&dpr=2&q=80',
// 		initials: 'JD',
// 	},
// 	{
// 		name: 'Jill Doe',
// 		username: 'jilldoe',
// 		following: '256',
// 		followers: '148',
// 		content: 'How to use custom fonts with Storybook',
// 		description: 'Sharing my journey on Storybook, Next JS and Tailwind CSS',
// 		date: '5h',
// 		src: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?ixlib=rb-1.2.1&w=128&h=128&dpr=2&q=80',
// 		initials: 'JD',
// 	},
// 	{
// 		name: 'Jeff Doe',
// 		username: 'jeffdoe',
// 		following: '232',
// 		followers: '89',
// 		content: 'Why use Storybook?',
// 		description: 'Learning and building projects with Next JS',
// 		date: '6h',
// 		src: 'https://images.unsplash.com/photo-1642060603505-e716140d45d2?ixlib=rb-1.2.1&w=128&h=128&dpr=2&q=80',
// 		initials: 'JD',
// 	},
// 	{
// 		name: 'Jean Doe',
// 		username: 'jeandoe',
// 		following: '186',
// 		followers: '90',
// 		content: 'Vercel and Netlify are pretty cool',
// 		description: 'Radix UI Avenger',
// 		date: '7h',
// 		src: 'https://images.unsplash.com/photo-1597248374161-426f0d6d2fc9?ixlib=rb-1.2.1&w=128&h=128&dpr=2&q=80',
// 		initials: 'JD',
// 	},
// 	{
// 		name: 'Jack Doe',
// 		username: 'jackdoe',
// 		following: '56',
// 		followers: '24',
// 		content: 'Webflow community is awesome',
// 		description: 'Currently redesigning my portfolio for the 8th time today',
// 		date: '8h',
// 		src: '',
// 		initials: 'JD',
// 	},
// 	{
// 		name: 'Jenny Doe',
// 		username: 'jennydoe',
// 		following: '56',
// 		followers: '23',
// 		content: 'Radix UI is nice to integrate',
// 		description: 'Figma and Next JS aficionado',
// 		date: '9h',
// 		src: 'https://images.unsplash.com/photo-1597004897768-c503466472cc?ixlib=rb-1.2.1&w=128&h=128&dpr=2&q=80',
// 		initials: 'JD',
// 	},
// ];

// interface FeedProp {
// 	searchKeyword: string,
// }

// interface NBASubquery {
//     subqueries: string[];
//     description: string;
// }

// const FeedV2 = ({searchKeyword}: FeedProp) => {
// 	const [posts, setPosts] = useState<PostItem[]>([]);
//     const [loading, setLoading] = useState<boolean>(true);
//     const [error, setError] = useState<string>('');
// 	// const [data, setData] = useState<NBASubquery | null>(null);
//     // const [error, setError] = useState<string>('');

// 	// useEffect(() => {
//     //     fetch('http://127.0.0.1:4000/search', {
//     //         method: 'POST',
//     //         headers: {
//     //             'Content-Type': 'application/json',
//     //         },
//     //         body: JSON.stringify({ query: 'NBA players' }),
//     //     })
//     //     .then(response => {
//     //         if (!response.ok) {
//     //             throw new Error('Network response was not ok');
//     //         }
//     //         return response.json();
//     //     })
//     //     .then(data => {
//     //         console.log(data);
//     //         setData(data[0]); // Assuming we're interested in the first element of the returned array
//     //     })
//     //     .catch(error => {
//     //         console.error('There was a problem with your fetch operation:', error);
//     //         setError(error.message);
//     //     });
//     // }, []);

// 	// if (error) {
//     //     return <div>Error: {error}</div>;
//     // }

//     // if (!data) {
//     //     return <div>Loading...</div>;
//     // }

// 	useEffect(() => {
//         const fetchData = async () => {
//             try {
//                 const response = await fetch('http://127.0.0.1:4000/search', {
//                     method: 'POST',
//                     headers: {
//                         'Content-Type': 'application/json',
//                     },
//                     body: JSON.stringify({ query: searchKeyword }),
//                 });
//                 if (!response.ok) {
//                     throw new Error('Failed to fetch data');
//                 }
//                 const data = await response.json();
//                 setPosts(data.posts);
//                 setLoading(false);
//             } catch (error) {
//                 setError(error.message);
//                 setLoading(false);
//             }
//         };

//         fetchData();
//     }, [searchKeyword]);

//     if (loading) {
//         return <Loading />;
//     }

//     if (error) {
//         return <div>Error: {error}</div>;
//     }

// 	return (
// 	<Suspense fallback={<Loading />}>
// 		<ul className="[&_p:last-child]:text-slate-500 [&_p:first-child]:text-lg divide-y divide-slate-200">
// 			{items.map(
// 				(
// 					{
// 						name,
// 						username,
// 						content,
// 						date,
// 						src,
// 						initials,
// 						image,
// 						following,
// 						followers,
// 						description,
// 					},
// 					i,
// 				) => (
// 					<li key={`username-${i}`} className="p-4">
// 						<Post
// 							name={name}
// 							username={username}
// 							content={content}
// 							date={date}
// 							src={src}
// 							initials={initials}
// 							description={description}
// 							followers={followers}
// 							following={following}
// 						>
// 							{image}
// 						</Post>
// 					</li>
// 				),
// 			)}
// 		</ul>
// 	</Suspense>
// );
// }

// export default FeedV2;

// function Loading() {
// 	return <h2>Loading...</h2>;
// }
