import React from 'react';
import {
  CssBaseline,
  Box,
  AppBar,
  Toolbar,
  Typography,
  Container,
  Paper,
  Tabs,
  Tab,
} from '@mui/material';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { ModelList } from './components/ModelList';
import { ServerList } from './components/ServerList';

const queryClient = new QueryClient();

function App() {
  const [tabValue, setTabValue] = React.useState(0);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <QueryClientProvider client={queryClient}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              HADES Model Management
            </Typography>
          </Toolbar>
        </AppBar>
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
          <Paper sx={{ p: 2 }}>
            <Tabs value={tabValue} onChange={handleTabChange} sx={{ mb: 2 }}>
              <Tab label="Models" />
              <Tab label="Servers" />
            </Tabs>
            {tabValue === 0 && <ModelList />}
            {tabValue === 1 && <ServerList />}
          </Paper>
        </Container>
      </Box>
      <ToastContainer position="bottom-right" />
    </QueryClientProvider>
  );
}

export default App;
