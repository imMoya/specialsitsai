export interface TickerData {
    ticker: string;
    num_filings: number;
    latest_filing_date: string;
  }
  
  export interface DatasetInfo {
    total_files: number;
    tickers: TickerData[];
  }
  
  export interface SummaryData {
    oddlots: DatasetInfo;
    spinoffs: DatasetInfo;
  }