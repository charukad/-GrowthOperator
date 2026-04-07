import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useParams } from 'react-router-dom';
import api from '../../services/api';
import { Loader2, PenTool, Layout, Lightbulb, Type, Video, ChevronDown, ChevronUp, FileText } from 'lucide-react';

export const IdeaWorkspace: React.FC = () => {
  const { workspaceId } = useParams<{ workspaceId: string }>();
  const queryClient = useQueryClient();
  const [selectedIdeaId, setSelectedIdea] = useState<string | null>(null);
  const [expandedVariant, setExpandedVariant] = useState<string | null>(null);

  const { data: ideas, isLoading } = useQuery({
    queryKey: ['ideas', workspaceId],
    queryFn: async () => {
      const response = await api.get(`/ideas/?workspace_id=${workspaceId}`);
      return response.data;
    },
    enabled: !!workspaceId,
  });

  const generateHooksMutation = useMutation({
    mutationFn: async ({ ideaId, platform }: { ideaId: string, platform: string }) => {
      const response = await api.post(`/ideas/${ideaId}/hooks/generate`, { platform, count: 3 });
      return { ideaId, hooks: response.data.hooks };
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ideas', workspaceId] });
    },
  });

  const generateCaptionMutation = useMutation({
    mutationFn: async (variantId: string) => {
      const response = await api.post(`/ideas/variants/${variantId}/generate-caption`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ideas', workspaceId] });
    },
  });

  const generateScriptMutation = useMutation({
    mutationFn: async (variantId: string) => {
      const response = await api.post(`/ideas/variants/${variantId}/generate-script`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['ideas', workspaceId] });
    },
  });

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-full">
        <Loader2 className="animate-spin h-8 w-8 text-indigo-500" />
      </div>
    );
  }

  const selectedIdea = ideas?.find((i: any) => i.id === selectedIdeaId);

  return (
    <div className="p-8 max-w-7xl mx-auto flex gap-8 h-[calc(100vh-4rem)]">
      {/* Ideas List */}
      <div className="w-1/3 flex flex-col bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div className="p-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center">
          <h2 className="font-semibold text-gray-800 flex items-center">
            <Lightbulb className="w-4 h-4 mr-2 text-yellow-500" />
            Content Ideas
          </h2>
          <span className="bg-gray-200 text-gray-700 py-0.5 px-2 rounded-full text-xs font-medium">
            {ideas?.length || 0}
          </span>
        </div>
        
        <div className="flex-1 overflow-y-auto p-2 space-y-2">
          {ideas?.map((idea: any) => (
            <div
              key={idea.id}
              onClick={() => setSelectedIdea(idea.id)}
              className={`p-3 rounded-md cursor-pointer border transition-colors ${
                selectedIdeaId === idea.id 
                  ? 'bg-indigo-50 border-indigo-200' 
                  : 'bg-white border-gray-100 hover:border-indigo-100 hover:bg-gray-50'
              }`}
            >
              <h3 className={`text-sm font-medium line-clamp-2 ${selectedIdeaId === idea.id ? 'text-indigo-900' : 'text-gray-900'}`}>
                {idea.title}
              </h3>
              <p className="text-xs text-gray-500 mt-1 flex items-center gap-2">
                <span className="capitalize">{idea.status}</span>
                {idea.variants?.length > 0 && (
                  <span className="text-indigo-600 bg-indigo-100 px-1.5 rounded text-[10px]">
                    {idea.variants.length} variant{idea.variants.length !== 1 ? 's' : ''}
                  </span>
                )}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Idea Detail Panel */}
      <div className="w-2/3 bg-white rounded-lg shadow-sm border border-gray-200 overflow-y-auto">
        {selectedIdea ? (
          <div className="p-6">
            <h1 className="text-2xl font-bold text-gray-900 mb-6">{selectedIdea.title}</h1>
            
            <div className="space-y-6">
              <div>
                <h3 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">Strategy Brief</h3>
                <div className="bg-gray-50 p-4 rounded-md text-gray-800 text-sm leading-relaxed border border-gray-100">
                  {selectedIdea.brief}
                </div>
              </div>

              <div>
                <h3 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-2">The Viral Angle</h3>
                <div className="bg-indigo-50 border border-indigo-100 p-4 rounded-md text-indigo-900 text-sm font-medium">
                  {selectedIdea.angle}
                </div>
              </div>

              <div className="pt-6 border-t border-gray-200">
                <h3 className="text-lg font-bold text-gray-900 flex items-center mb-4">
                  <Layout className="w-5 h-5 mr-2 text-indigo-500" />
                  Content Variants
                </h3>

                <div className="space-y-4">
                  {selectedIdea.variants?.length > 0 ? selectedIdea.variants.map((variant: any) => (
                    <div key={variant.id} className="border border-gray-200 rounded-lg overflow-hidden shadow-sm">
                      <div 
                        className="bg-gray-50 px-4 py-3 border-b border-gray-200 flex justify-between items-center cursor-pointer hover:bg-gray-100"
                        onClick={() => setExpandedVariant(expandedVariant === variant.id ? null : variant.id)}
                      >
                        <div className="flex items-center">
                          <span className="font-bold text-gray-700 capitalize mr-3">{variant.platform}</span>
                          <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold uppercase ${
                            variant.status === 'generated' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                          }`}>
                            {variant.status}
                          </span>
                        </div>
                        {expandedVariant === variant.id ? <ChevronUp className="w-4 h-4 text-gray-400" /> : <ChevronDown className="w-4 h-4 text-gray-400" />}
                      </div>
                      
                      {expandedVariant === variant.id && (
                        <div className="p-4 space-y-4 bg-white animate-in slide-in-from-top-1 duration-200">
                          {/* Hook Section */}
                          <div>
                            <p className="text-[10px] font-black text-gray-400 uppercase mb-1">Hook</p>
                            {variant.hook ? (
                              <p className="text-sm text-gray-800 font-medium italic">"{variant.hook}"</p>
                            ) : (
                              <button
                                onClick={() => generateHooksMutation.mutate({ ideaId: selectedIdea.id, platform: variant.platform })}
                                disabled={generateHooksMutation.isPending}
                                className="text-xs text-indigo-600 font-bold hover:underline flex items-center"
                              >
                                <PenTool className="w-3 h-3 mr-1" /> Generate Hooks
                              </button>
                            )}
                          </div>

                          {/* Caption Section */}
                          <div className="pt-3 border-t border-gray-50">
                            <p className="text-[10px] font-black text-gray-400 uppercase mb-1">Caption</p>
                            {variant.caption ? (
                              <div className="text-sm text-gray-700 whitespace-pre-wrap bg-gray-50 p-3 rounded border border-gray-100">
                                {variant.caption}
                              </div>
                            ) : (
                              <button
                                onClick={() => generateCaptionMutation.mutate(variant.id)}
                                disabled={generateCaptionMutation.isPending || !variant.hook}
                                className="text-xs text-indigo-600 font-bold hover:underline flex items-center disabled:opacity-50"
                              >
                                <Type className="w-3 h-3 mr-1" /> {generateCaptionMutation.isPending ? 'Writing...' : 'Generate Caption'}
                              </button>
                            )}
                          </div>

                          {/* Script Section */}
                          <div className="pt-3 border-t border-gray-50">
                            <p className="text-[10px] font-black text-gray-400 uppercase mb-1">Video Script</p>
                            {variant.script_data?.scenes ? (
                              <div className="space-y-3">
                                {variant.script_data.scenes.map((scene: any) => (
                                  <div key={scene.scene_number} className="bg-indigo-50/30 p-3 rounded border border-indigo-100/50">
                                    <div className="flex justify-between mb-1">
                                      <span className="text-[10px] font-bold text-indigo-600 uppercase">Scene {scene.scene_number}</span>
                                      <span className="text-[10px] text-gray-400">{scene.duration}s</span>
                                    </div>
                                    <p className="text-xs text-gray-800 mb-1"><span className="font-bold">Visual:</span> {scene.visual}</p>
                                    <p className="text-xs text-gray-600 italic"><span className="font-bold not-italic">Audio:</span> {scene.audio}</p>
                                  </div>
                                ))}
                              </div>
                            ) : (
                              <button
                                onClick={() => generateScriptMutation.mutate(variant.id)}
                                disabled={generateScriptMutation.isPending || !variant.hook}
                                className="text-xs text-indigo-600 font-bold hover:underline flex items-center disabled:opacity-50"
                              >
                                <Video className="w-3 h-3 mr-1" /> {generateScriptMutation.isPending ? 'Scripting...' : 'Generate Video Script'}
                              </button>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  )) : (
                    <div className="text-center py-12 bg-gray-50 rounded-lg border border-dashed border-gray-300">
                      <FileText className="mx-auto h-10 w-10 text-gray-300" />
                      <p className="mt-2 text-sm text-gray-500">No platform variants yet.</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-gray-400">
            <Lightbulb className="w-16 h-16 mb-4 text-gray-200" />
            <p className="font-medium">Select a content idea to start crafting</p>
          </div>
        )}
      </div>
    </div>
  );
};
