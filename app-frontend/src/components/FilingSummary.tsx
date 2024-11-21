import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getSummaryData } from '../services/api';
import { SummaryContainer, Card, CardTitle, TickerList, TickerItem } from '../styles/SummaryStyles';
import { SummaryData } from '../types';

export const FilingSummary: React.FC = () => {
  const [summaryData, setSummaryData] = useState<SummaryData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getSummaryData();
        setSummaryData(data);
      } catch (error) {
        console.error('Error fetching summary data:', error);
      }
    };

    fetchData();
  }, []);

  if (!summaryData) return <div>Loading...</div>;

  return (
    <SummaryContainer>
      <Card>
        <CardTitle>Oddlots</CardTitle>
        <p>Total Files: {summaryData.oddlots.total_files}</p>
        <h3>Tickers:</h3>
        <TickerList>
          {summaryData.oddlots.tickers.map((ticker) => (
            <TickerItem key={ticker.ticker}>
              <Link to={`/oddlots/${ticker.ticker}`}>
                {ticker.ticker} ({ticker.num_filings} filings, latest: {ticker.latest_filing_date})
              </Link>
            </TickerItem>
          ))}
        </TickerList>
      </Card>

      <Card>
        <CardTitle>Spinoffs</CardTitle>
        <p>Total Files: {summaryData.spinoffs.total_files}</p>
        <h3>Tickers:</h3>
        <TickerList>
          {summaryData.spinoffs.tickers.map((ticker) => (
            <TickerItem key={ticker.ticker}>
              <Link to={`/spinoffs/${ticker.ticker}`}>
                {ticker.ticker} ({ticker.num_filings} filings, latest: {ticker.latest_filing_date})
              </Link>
            </TickerItem>
          ))}
        </TickerList>
      </Card>
    </SummaryContainer>
  );
};