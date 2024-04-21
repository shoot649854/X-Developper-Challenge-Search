import React, { useEffect, useState } from 'react';
import Image from 'next/image';
import Post from '@ui/Post';
import { ReactNode } from 'react';
import { Suspense } from 'react';
import { useRouter } from 'next/router';
import grokLogo from '../../public/grok-logo.png';

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
			<div className="bg-slate-900 p-4 rounded-lg shadow mb-4">
				<div className="flex">
					<div className="flex-1 min-w-[30px] mr-2">
						<Image
							src={grokLogo}
							alt="Grok Logo"
							className="width: 100%; height: auto; object-fit: cover;"
							width={30}
							height={30}
						/>
					</div>
					<div>
						<div className="flex flex-row space-x-1 items-center">
							<div className="text-overflow: unset; color: rgb(231, 233, 234);">
								<span className="text-overflow: unset; color: rgb(231, 233, 234);">
									<span className="text-overflow text-white font-bold">
										Grok
									</span>
								</span>
							</div>
							<div className="text-overflow: unset; color: rgb(231, 233, 234)">
								<span className="text-overflow: unset;">
									<svg
										viewBox="0 0 22 22"
										aria-label="Verified account"
										role="img"
										className="height: calc(1.0625em); width: calc(1.0625em);"
										style={{ height: '15px', width: '15px' }}
									>
										<g>
											<linearGradient
												gradientUnits="userSpaceOnUse"
												id="8-a"
												x1="4.411"
												x2="18.083"
												y1="2.495"
												y2="21.508"
											>
												<stop offset="0" stop-color="#f4e72a"></stop>
												<stop offset=".539" stop-color="#cd8105"></stop>
												<stop offset=".68" stop-color="#cb7b00"></stop>
												<stop offset="1" stop-color="#f4ec26"></stop>
												<stop offset="1" stop-color="#f4e72a"></stop>
											</linearGradient>
											<linearGradient
												gradientUnits="userSpaceOnUse"
												id="8-b"
												x1="5.355"
												x2="16.361"
												y1="3.395"
												y2="19.133"
											>
												<stop offset="0" stop-color="#f9e87f"></stop>
												<stop offset=".406" stop-color="#e2b719"></stop>
												<stop offset=".989" stop-color="#e2b719"></stop>
											</linearGradient>
											<g clip-rule="evenodd" fill-rule="evenodd">
												<path
													d="M13.324 3.848L11 1.6 8.676 3.848l-3.201-.453-.559 3.184L2.06 8.095 3.48 11l-1.42 2.904 2.856 1.516.559 3.184 3.201-.452L11 20.4l2.324-2.248 3.201.452.559-3.184 2.856-1.516L18.52 11l1.42-2.905-2.856-1.516-.559-3.184zm-7.09 7.575l3.428 3.428 5.683-6.206-1.347-1.247-4.4 4.795-2.072-2.072z"
													fill="url(#8-a)"
												></path>
												<path
													d="M13.101 4.533L11 2.5 8.899 4.533l-2.895-.41-.505 2.88-2.583 1.37L4.2 11l-1.284 2.627 2.583 1.37.505 2.88 2.895-.41L11 19.5l2.101-2.033 2.895.41.505-2.88 2.583-1.37L17.8 11l1.284-2.627-2.583-1.37-.505-2.88zm-6.868 6.89l3.429 3.428 5.683-6.206-1.347-1.247-4.4 4.795-2.072-2.072z"
													fill="url(#8-b)"
												></path>
												<path
													d="M6.233 11.423l3.429 3.428 5.65-6.17.038-.033-.005 1.398-5.683 6.206-3.429-3.429-.003-1.405.005.003z"
													fill="#d18800"
												></path>
											</g>
										</g>
									</svg>
								</span>
							</div>
							<div>
								<Image
									alt=""
									draggable="false"
									src="https://pbs.twimg.com/profile_images/1769430779845611520/lIgjSJGU_bigger.jpg"
									className="height: calc(1.0625em); width: calc(1.0625em); border-radius: 2px;"
									height={15}
									width={15}
								/>
							</div>
							<div className="text-slate-500 text-sm">@grok</div>
						</div>
						<p className="text-white">
							{description
								? description.description
								: 'No context available for this search.'}
						</p>
					</div>
				</div>
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
