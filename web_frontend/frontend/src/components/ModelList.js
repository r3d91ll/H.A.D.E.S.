import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Stack,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  CloudDownload,
  PlayArrow,
  Stop,
  Refresh,
} from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { modelApi } from '../api/modelApi';
import { toast } from 'react-toastify';

const statusColors = {
  downloading: 'info',
  loading: 'warning',
  ready: 'success',
  unloading: 'warning',
  error: 'error',
};

export const ModelList = () => {
  const queryClient = useQueryClient();

  const { data: models = [], isLoading } = useQuery({
    queryKey: ['models'],
    queryFn: modelApi.listModels,
    refetchInterval: 5000,
  });

  const downloadMutation = useMutation({
    mutationFn: modelApi.downloadModel,
    onSuccess: () => {
      queryClient.invalidateQueries(['models']);
      toast.success('Model download started');
    },
    onError: (error) => {
      toast.error(`Failed to download model: ${error.message}`);
    },
  });

  const loadMutation = useMutation({
    mutationFn: modelApi.loadModel,
    onSuccess: () => {
      queryClient.invalidateQueries(['models']);
      toast.success('Model loaded successfully');
    },
    onError: (error) => {
      toast.error(`Failed to load model: ${error.message}`);
    },
  });

  const unloadMutation = useMutation({
    mutationFn: modelApi.unloadModel,
    onSuccess: () => {
      queryClient.invalidateQueries(['models']);
      toast.success('Model unloaded successfully');
    },
    onError: (error) => {
      toast.error(`Failed to unload model: ${error.message}`);
    },
  });

  if (isLoading) {
    return <Typography>Loading models...</Typography>;
  }

  return (
    <Box>
      <Stack spacing={2}>
        {models.map((model) => (
          <Card key={model.model_name}>
            <CardContent>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Box>
                  <Typography variant="h6">{model.model_name}</Typography>
                  <Chip
                    label={model.status}
                    color={statusColors[model.status]}
                    size="small"
                    sx={{ mt: 1 }}
                  />
                </Box>
                <Stack direction="row" spacing={1}>
                  <Tooltip title="Download Model">
                    <IconButton
                      onClick={() => downloadMutation.mutate(model.model_name)}
                      disabled={model.status !== 'error' && model.status !== undefined}
                    >
                      <CloudDownload />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Load Model">
                    <IconButton
                      onClick={() => loadMutation.mutate(model.model_name)}
                      disabled={model.status !== 'ready'}
                    >
                      <PlayArrow />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Unload Model">
                    <IconButton
                      onClick={() => unloadMutation.mutate(model.model_name)}
                      disabled={model.status !== 'ready'}
                    >
                      <Stop />
                    </IconButton>
                  </Tooltip>
                </Stack>
              </Stack>
              {model.error && (
                <Typography color="error" variant="body2" sx={{ mt: 1 }}>
                  Error: {model.error}
                </Typography>
              )}
            </CardContent>
          </Card>
        ))}
      </Stack>
    </Box>
  );
};
