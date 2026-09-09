
   from typing import TypedDict
   from langgraph.graph import StateGraph, START, END
   import sqlite3
   from langgraph.checkpoint.sqlite import SqliteSaver

   class TestCaseReviewState(TypedDict):
    requirement: str
    test_cases: list
    reviewer: str
    approved: bool
    feedback: str
    revision_count: int

   def generate_test_cases(state: TestCaseReviewState) ->   TestCaseReviewState:
    """生成测试用例"""
    print("✍️  生成测试用例...")
    state["test_cases"] = [
        {"id":   "TC_001", "title": "正常登录",   "steps": ["输入用户名", "输入密码", "点击登录"]},
        {"id":   "TC_002", "title": "错误密码",   "steps": ["输入用户名", "输入错误密码", "点击登录"]},
    ]
    return state

   def human_review(state: TestCaseReviewState) -> TestCaseReviewState:
    """人工审核"""
    print("\n" +   "="*60)
    print("👤 测试用例审核")
    print("="*60)
    print(f"需求: {state['requirement']}")
    print(f"\n生成的测试用例:")
    for tc in   state["test_cases"]:
        print(f"  - {tc['id']}: {tc['title']}")
    
    print("\n请审核:")
    print("1. 批准（输入 'y'）")
    print("2. 需要修改（输入 'n'）")
    
    choice = input("\n您的决定: ").strip().lower()
    if choice == 'y':
        state["approved"] =   True
        state["feedback"] =   ""
        print("✅ 已批准")
    else:
        state["approved"] =   False
        state["feedback"] =   input("请提供修改意见: ")
        print("📝 反馈已记录")
    
    return state

   def revise_test_cases(state: TestCaseReviewState) -> TestCaseReviewState:
    """根据反馈修订测试用例"""
    print(f"\n🔧 根据反馈修订: {state['feedback']}")
    # 模拟修订：添加新的测试用例
      state["test_cases"].append({
        "id":   f"TC_{len(state['test_cases']) + 1:03d}",
        "title": f"根据反馈添加: {state['feedback']}",
        "steps": ["步骤1", "步骤2"]
    })
    state["revision_count"]   += 1
    return state

   def check_approval(state: TestCaseReviewState) -> str:
    """检查是否批准"""
    if state["approved"]:
        return "complete"
    elif   state["revision_count"] >= 3:
        print("⚠️  已达最大修订次数，强制完成")
        return "complete"
    else:
        return "revise"

   # 构建工作流
   workflow = StateGraph(TestCaseReviewState)
   workflow.add_node("generate", generate_test_cases)
   workflow.add_node("review", human_review)
   workflow.add_node("revise", revise_test_cases)

   workflow.set_entry_point("generate")
   workflow.add_edge("generate", "review")
   workflow.add_conditional_edges(
    "review",
    check_approval,
    {
        "complete": END,
        "revise":   "revise"
    }
   )
   workflow.add_edge("revise", "review")

   # 使用持久化
   conn = sqlite3.connect("test_case_review.db",   check_same_thread=False)
   checkpointer = SqliteSaver(conn)

   app = workflow.compile(checkpointer=checkpointer)

   # 打印工作流图
   print("\n" + "="*70)
   print("📊 工作流图结构")
   print("="*70)
   graph = app.get_graph()
   print(graph.draw_mermaid())
   print("\n" + "="*70)

   result = app.invoke({
    "requirement": "用户登录功能",
    "test_cases": [],
    "reviewer": "",
    "approved": False,
    "feedback": "",
    "revision_count": 0
   }, config={"configurable": {"thread_id":   "review_001"}})

   print(f"\n最终测试用例数:   {len(result['test_cases'])}")
   print(f"修订次数: {result['revision_count']}")