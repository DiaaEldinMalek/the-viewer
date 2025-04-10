'use client'; // Required for hooks

import SearchBar from '../src/components/SearchBar';
import PreviousBooksList from '../src/components/PreviousBooksList'
import PingButton from '@/src/components/PingButton';
import GetBookByID from '@/src/components/GetBookByID';

export default function Home() {

  return (
    <div className="home-container">
      <div className="container">
        <main className="main">
          <SearchBar />
        </main>
      </div>


      <h1>{process.env.NEXT_PUBLIC_APP_NAME}</h1>
      <GetBookByID></GetBookByID>


      <div className="container">
        <main className="main">
          <PreviousBooksList />
        </main>
      </div>

      {/* Test Server Button */}
      <PingButton></PingButton>
    </div>
  );
}