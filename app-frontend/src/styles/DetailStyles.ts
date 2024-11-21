import styled from 'styled-components';

export const DetailContainer = styled.div`
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
`;

export const DetailRow = styled.div`
  margin: 15px 0;
  
  strong {
    display: block;
    margin-bottom: 5px;
    color: #333;
  }
  
  ul {
    margin: 0;
    padding-left: 20px;
  }
`;

export const BackLink = styled.div`
  margin-bottom: 20px;
  
  a {
    color: #0066cc;
    text-decoration: none;
    
    &:hover {
      text-decoration: underline;
    }
  }
`;