/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    env: {
      API_BASE_URL: process.env.NEXT_PUBLIC_BACKEND_API_BASE_URL,
    },
  };
  
export default nextConfig;