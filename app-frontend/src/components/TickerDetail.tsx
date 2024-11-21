import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getTickerDetails } from '../services/api';
import { Card, CardTitle } from '../styles/SummaryStyles';
import { DetailContainer, DetailRow, BackLink } from '../styles/DetailStyles';

interface TickerDetailData {
  dataset: string;
  ticker: string;
  details: {
    urls?: string[];
    filing_numbers?: string[];
    dates_filing?: string[];
    expiration_date?: string;
    lower_price?: string;
    currency?: string;
    oddlot_priority?: string;
    shareholder_requirements?: string;
    risks?: string;
    regulatory_approvals?: string;
    tax_consequences?: string;
  };
}

const formatLatestDate = (dates: string[] | undefined): string => {
  if (!dates || dates.length === 0) return 'N/A';
  const latestTimestamp = Math.max(...dates.map(date => new Date(date).getTime()));
  return new Date(latestTimestamp).toLocaleDateString();
};

export const TickerDetail: React.FC = () => {
  const { dataset, ticker } = useParams<{ dataset: string; ticker: string }>();
  const [detailData, setDetailData] = useState<TickerDetailData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDetails = async () => {
      if (dataset && ticker) {
        try {
          const data = await getTickerDetails(dataset, ticker);
          setDetailData(data);
          setError(null);
        } catch (error) {
          console.error('Error fetching ticker details:', error);
          setError('Failed to load ticker details. Please try again later.');
        }
      }
    };

    fetchDetails();
  }, [dataset, ticker]);

  if (error) return <div>{error}</div>;
  if (!detailData) return <div>Loading...</div>;

  return (
    <DetailContainer>
      <BackLink>
        <Link to="/">← Back to Summary</Link>
      </BackLink>
      <Card>
        <CardTitle>{detailData.ticker} Details</CardTitle>
        <DetailRow>
          <strong>Dataset:</strong> {detailData.dataset}
        </DetailRow>
        <DetailRow>
          <strong>Filing Links:</strong>
          <ul>
            {detailData.details.urls?.map((url, index) => (
              <li key={index}>
                <a 
                  href={url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                >
                  Filing {detailData.details.filing_numbers?.[index] || index + 1}
                </a>
              </li>
            )) || 'N/A'}
          </ul>
        </DetailRow>
        <DetailRow>
          <strong>Latest Filing Date:</strong> {formatLatestDate(detailData.details.dates_filing)}
        </DetailRow>
        <DetailRow>
          <strong>Expiration Date:</strong> {detailData.details.expiration_date || 'N/A'}
        </DetailRow>
        <DetailRow>
          <strong>Lower Price:</strong> {detailData.details.lower_price || 'N/A'}
        </DetailRow>
        <DetailRow>
          <strong>Currency:</strong> {detailData.details.currency || 'N/A'}
        </DetailRow>
        <DetailRow>
          <strong>Odd Lot Priority:</strong> {detailData.details.oddlot_priority || 'N/A'}
        </DetailRow>
        <DetailRow>
          <strong>Shareholder Requirements:</strong> {detailData.details.shareholder_requirements || 'N/A'}
        </DetailRow>
        <DetailRow>
          <strong>Risks:</strong> {detailData.details.risks || 'N/A'}
        </DetailRow>
        <DetailRow>
          <strong>Regulatory Approvals:</strong> {detailData.details.regulatory_approvals || 'N/A'}
        </DetailRow>
        <DetailRow>
          <strong>Tax Consequences:</strong> {detailData.details.tax_consequences || 'N/A'}
        </DetailRow>
      </Card>
    </DetailContainer>
  );
};