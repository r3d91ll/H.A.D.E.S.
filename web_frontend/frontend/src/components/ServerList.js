import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  IconButton,
  Chip,
  Stack,
  Tooltip,
} from '@mui/material';
import {
  PlayArrow,
  Stop,
  CheckCircle,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { serverApi } from '../api/serverApi';
import { toast } from 'react-toastify';

const statusColors = {
  starting: 'warning',
  running: 'success',
  stopped: 'error',
  error: 'error',
};

export const ServerList = () => {
  const queryClient = useQueryClient();

  const { data: serverList = { servers: [] }, isLoading } = useQuery({
    queryKey: ['servers'],
    queryFn: serverApi.listServers,
    refetchInterval: 5000,
  });

  const startMutation = useMutation({
    mutationFn: serverApi.startServer,
    onSuccess: () => {
      queryClient.invalidateQueries(['servers']);
      toast.success('Server started successfully');
    },
    onError: (error) => {
      toast.error(`Failed to start server: ${error.message}`);
    },
  });

  const stopMutation = useMutation({
    mutationFn: serverApi.stopServer,
    onSuccess: () => {
      queryClient.invalidateQueries(['servers']);
      toast.success('Server stopped successfully');
    },
    onError: (error) => {
      toast.error(`Failed to stop server: ${error.message}`);
    },
  });

  const healthMutation = useMutation({
    mutationFn: serverApi.checkHealth,
    onSuccess: () => {
      queryClient.invalidateQueries(['servers']);
      toast.success('Health check completed');
    },
    onError: (error) => {
      toast.error(`Health check failed: ${error.message}`);
    },
  });

  if (isLoading) {
    return <Typography>Loading servers...</Typography>;
  }

  return (
    <Box>
      <Stack spacing={2}>
        {serverList.servers.map((server) => (
          <Card key={server.server_id}>
            <CardContent>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Box>
                  <Typography variant="h6">
                    Server {server.server_id.slice(0, 8)}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {server.config.model_name} - Port {server.config.port}
                  </Typography>
                  <Chip
                    label={server.status}
                    color={statusColors[server.status]}
                    size="small"
                    sx={{ mt: 1 }}
                  />
                </Box>
                <Stack direction="row" spacing={1}>
                  <Tooltip title="Start Server">
                    <IconButton
                      onClick={() => startMutation.mutate(server.config)}
                      disabled={server.status === 'running' || server.status === 'starting'}
                    >
                      <PlayArrow />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Stop Server">
                    <IconButton
                      onClick={() => stopMutation.mutate(server.server_id)}
                      disabled={server.status === 'stopped'}
                    >
                      <Stop />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Health Check">
                    <IconButton
                      onClick={() => healthMutation.mutate(server.server_id)}
                      disabled={server.status !== 'running'}
                    >
                      <CheckCircle />
                    </IconButton>
                  </Tooltip>
                </Stack>
              </Stack>
              {server.error && (
                <Typography color="error" variant="body2" sx={{ mt: 1 }}>
                  Error: {server.error}
                </Typography>
              )}
            </CardContent>
          </Card>
        ))}
      </Stack>
    </Box>
  );
};
