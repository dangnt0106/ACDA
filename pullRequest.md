#### Function Name:
<!--Ví dụ: KT_AFR ATFM EDCT情報照会機能-->
#### Reviewer:
<!--Vui lòng điền tên người review-->
#### Review Date:
<!--Vui lòng điền ngày tháng hiện tại-->
#### Description of changes:
<!--Vui lòng mô tả chi tiết những thay đổi mà bạn đã thực hiện trong pull request này. Cung cấp bối cảnh và lý do cho sự thay đổi, nếu có thể.-->
#### LOC:<!--Vui lòng điền số dòng code tạo mới và chỉnh sửa (Không cần đếm số dòng code delete, file common, không chỉnh sửa)-->
### ✅ Checklist before merging#### Common Checklist- 
[ ] Đặt tên file và structure của source cũ giống với source mới (nên giống cả số lượng nếu được)  - (Example: `IrregularRegistUCControl` ⇒ `IrregularRegistUCControl.vue`)
- [ ] Have unnecessary logic and comments been removed?
- [ ] Have all debug codes been removed? (Example: `Console.log()`, `System.print()`)
- [ ] Have all code review tool warnings been resolved?
- [ ] Has the code been formatted?
- [ ] Are there comments for functions and complex logic?
- [ ] If there are discrepancies between the design and the old source, has it been confirmed with the PL or JP side?
- [ ] Before create pull request, did you rebase? (Trước khi tạo pull request, đã rebase chưa?)
- [ ] Nếu có sai khác logic giữa source và thiết kế liên hệ Long để note lại phần sai khác---
#### Vue.js Checklist
- [ ] Is the initialization process for each UC screen correctly following the **External Design Document**?
- [ ] Is the output processing for each UC screen correctly following the **External Design Document**?
- [ ] Is the event processing for each UC screen correctly following the **External Design Document**?
- [ ] Is the dummy data sufficient to test all cases?
- [ ] After changing the value of `VITE_MOCK_REQUEST`, can the API be successfully called to the backend?
- [ ] Does the report output follow the rules specified in the file 
**「【新運航管理】帳票UI規約.docx」** (Margin, layout, A4, A3, etc.)?
- [ ] Has it been confirmed with the PL or JP side before modifying common files?  - (Ngoài folder [view, testdata, router], các file thuộc các folder còn lại là common)
### 📌 Additional notes (if any)
<!-- Ghi chú khác (nếu cần) -->