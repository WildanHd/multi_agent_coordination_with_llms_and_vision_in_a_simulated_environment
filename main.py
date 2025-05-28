from agents.vision_agent import VisionAgent
from agents.rule_based_processing_agent import plan_route_rule_based
#from agents.openrouter_processing_agent import plan_route_with_llm
from agents.action_agent import animate_route_on_map

# Example usage
if __name__ == "__main__":
    image_file = "assets/generated_maps/generated_map.png"
    vision_output_file = "output/vision_output.json"
    rule_based_processing_output_file = "output/rule_based_processing_output.json"
    openrouter_processing_output_file = "output/openrouter_processing_output.json"

    VisionAgent.run_vision_agent(image_file, vision_output_file)

    actions = plan_route_rule_based(
    vision_output_path=vision_output_file,
    save_path=rule_based_processing_output_file)

    print("Rule based route has been saved! Here's the plan:")
    for step in actions:
        print("-", step)

    #plan_route_with_llm(vision_output_path=vision_output_file)
    #print("LLM based route has been saved!")

    print("Let's take the actions!")
    animate_route_on_map(
        image_file,
        vision_output_file,
        rule_based_processing_output_file
    )
