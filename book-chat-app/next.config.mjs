/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    env: {
      API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL,
    },
  };
  
  module.exports = nextConfig;