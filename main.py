import os

from agent import get_graph
from inputs import from_github
from langchain_core.messages import HumanMessage
from tools import get_pr_metadata

from composio import Action

import logging
logging.getLogger().setLevel(logging.DEBUG)

# TODO: 
# 1. API_KEY
# 2. Log
# 3. RAG with langchain

def main() -> None:
    """Run the agent."""
    owner, repo_name, pull_number = from_github()
    print("\n*****************************\n",owner, repo_name, pull_number,"\n*****************************\n")

    repo_path = f"/Users/lingyawen1/lyw/AGI/2_Agents/composio_test/{repo_name}"

    graph, composio_toolset = get_graph(repo_path)

    composio_toolset.execute_action(
        action=Action.FILETOOL_GIT_CLONE,
        params={"repo_name": f"{owner}/{repo_name}"},
    )
    composio_toolset.execute_action(
        action=Action.FILETOOL_CHANGE_WORKING_DIRECTORY,
        params={"path": "/Users/lingyawen1/lyw/AGI/2_Agents/composio_test/"}, # repo_path},
    )
    composio_toolset.execute_action(
        action=Action.CODE_ANALYSIS_TOOL_CREATE_CODE_MAP,
        params={},
    )

    # response = composio_toolset.execute_action(
    #     action=get_pr_metadata,
    #     params={
    #         "owner": "ComposioHQ",
    #         "repo": "composio",
    #         "pull_number": "766",
    #         "thought": "Get the metadata for the PR",
    #     },
    # )
    # base_commit = response["data"]["metadata"]["base"]["sha"]

    # composio_toolset.execute_action(
    #     action=Action.FILETOOL_GIT_CLONE,
    #     params={
    #         "repo_name": "ComposioHQ/composio",
    #         "just_reset": True,
    #         "commit_id": base_commit,
    #     },
    # )

    run_result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=f"You have {owner}/{repo_name} cloned at your current working directory. Review PR {pull_number} on this repository and create comments on the same PR"
                )
            ]
        },
        {"recursion_limit": 50},
    )

    print(run_result)


if __name__ == "__main__":
    main()
