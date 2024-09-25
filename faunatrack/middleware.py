# class PythagoreMiddleware(Middleware):

#     def __call__(request):
#         try: 
#             self.get_response()
#         except ValidationError as e:
#             if e == "unique_together":
#                 return HttpResponse("C'est n'importe quoi les ours à Paris")
