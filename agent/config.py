from pydantic import BaseModel, Field



class Configuration(BaseModel):
    model: str = Field(
        default="gemini-2.5-flash",
        description="The model to use for the agent. Options include 'gemini-2.5-flash', 'gemini-2.5-pro', etc."
    )
    temperature: float = Field(
        default=0.7,
        description="The temperature to use for the agent's responses. Higher values make the output more random."
    )   