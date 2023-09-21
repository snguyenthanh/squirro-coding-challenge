import { QueryClient, QueryClientProvider } from 'react-query';
import StoreList from './components/StoreList';
import './App.css';

const queryClient = new QueryClient();

function App() {
  
  return (
    <QueryClientProvider client={queryClient}>
      <StoreList />
    </QueryClientProvider>
  );
}

export default App;
