import json
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from app.core.config import settings
from app.models.trend import Trend
from app.models.brand import Brand
from loguru import logger

class ContentEngineService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o" # Use a high-quality model for ideation

    async def generate_ideas_from_trend(
        self, trend: Trend, brand: Optional[Brand] = None, count: int = 3
    ) -> List[Dict[str, Any]]:
        brand_context = ""
        if brand:
            brand_context = f"""
            Target Brand Information:
            - Name: {brand.name}
            - Niche: {brand.niche}
            - Tone: {brand.tone_profile}
            - Audience: {brand.target_audience}
            - Pillars: {brand.content_pillars}
            """

        prompt = f"""
        You are a viral social media strategist. 
        Analyze the following trend and generate {count} unique content ideas.
        
        Trend: {trend.title}
        Summary: {trend.summary}
        {brand_context}
        
        For each idea, provide:
        1. Title (hooky and short)
        2. Brief (the core concept)
        3. Angle (the unique perspective or "why" it will work)
        4. Platform (e.g., Reels, TikTok, Twitter/X)
        
        Return the response ONLY as a JSON array of objects.
        Format:
        [
          {{
            "title": "...",
            "brief": "...",
            "angle": "...",
            "platform": "..."
          }}
        ]
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a viral content ideation expert. You output only raw JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )
            
            content = response.choices[0].message.content
            # The model might return a wrapper object like {"ideas": [...]} depending on response_format
            data = json.loads(content)
            if isinstance(data, dict) and "ideas" in data:
                return data["ideas"]
            elif isinstance(data, list):
                return data
            return data.get("ideas", []) if isinstance(data, dict) else []
            
        except Exception as e:
            logger.error(f"Error generating content ideas: {e}")
            raise e

    async def generate_hooks_for_idea(
        self, idea_brief: str, platform: str, count: int = 3, brand: Optional[Brand] = None
    ) -> List[str]:
        brand_context = ""
        if brand:
            brand_context = f"""
            Target Brand Information:
            - Name: {brand.name}
            - Niche: {brand.niche}
            - Tone: {brand.tone_profile}
            - Audience: {brand.target_audience}
            """

        prompt = f"""
        You are an expert copywriter and hook specialist for {platform}.
        Generate {count} highly engaging, scroll-stopping hooks for the following content idea:
        
        Idea Brief: {idea_brief}
        {brand_context}
        
        The hooks must be native to {platform} (e.g., short and punchy for TikTok, text-based for Twitter).
        
        Return the response ONLY as a JSON array of strings.
        Format:
        [
          "Hook 1",
          "Hook 2",
          "Hook 3"
        ]
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a hook generation expert. You output only raw JSON arrays of strings."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" } # Sometimes it struggles with raw array in json_object mode, we might need to wrap it.
            )
            
            content = response.choices[0].message.content
            data = json.loads(content)
            
            if isinstance(data, dict):
                # Look for the first list in the dict
                for val in data.values():
                    if isinstance(val, list):
                        return [str(v) for v in val]
            elif isinstance(data, list):
                return [str(v) for v in data]
                
            return []
            
        except Exception as e:
            logger.error(f"Error generating hooks: {e}")
            raise e

    async def generate_caption(
        self, idea_brief: str, hook: str, platform: str, brand: Optional[Brand] = None
    ) -> str:
        brand_context = ""
        if brand:
            brand_context = f"Brand Tone: {brand.tone_profile}. Audience: {brand.target_audience}."

        prompt = f"""
        Write a high-converting caption for {platform} based on this idea and hook.
        
        Idea: {idea_brief}
        Hook: {hook}
        {brand_context}
        
        The caption should:
        1. Expand on the hook immediately.
        2. Provide value or build curiosity.
        3. Include a clear Call to Action (CTA).
        4. Use relevant hashtags (max 5).
        
        Return ONLY the raw caption text.
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a social media copywriting expert."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating caption: {e}")
            raise e

    async def generate_script(
        self, idea_brief: str, hook: str, platform: str, brand: Optional[Brand] = None
    ) -> Dict[str, Any]:
        brand_context = ""
        if brand:
            brand_context = f"Brand Tone: {brand.tone_profile}."

        prompt = f"""
        Create a detailed, scene-by-scene video script for {platform} (short-form video).
        
        Idea: {idea_brief}
        Hook: {hook}
        {brand_context}
        
        Return the script as a structured JSON object:
        {{
          "title": "...",
          "estimated_duration": "...",
          "scenes": [
            {{
              "scene_number": 1,
              "visual": "What should be on screen (actions, text overlays)",
              "audio": "Narration or background sound description",
              "duration": "Duration in seconds"
            }}
          ]
        }}
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a viral video scriptwriter. You output ONLY raw JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Error generating script: {e}")
            raise e

content_engine = ContentEngineService()
