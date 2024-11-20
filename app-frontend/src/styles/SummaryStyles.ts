import styled from 'styled-components';

export const SummaryContainer = styled.div`
  display: flex;
  gap: 20px;
  justify-content: center;
`;

export const Card = styled.div`
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

export const CardTitle = styled.h2`
  margin-top: 0;
  color: #333;
`;

export const TickerList = styled.ul`
  list-style: none;
  padding: 0;
`;

export const TickerItem = styled.li`
  margin: 8px 0;
  padding: 8px;
  background: #f5f5f5;
  border-radius: 4px;
`;