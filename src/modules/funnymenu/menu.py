@@ .. @@
 from src.util.ui import ui
+from src.modules.funnymenu.funnystuff import funnystuff
 
 class funnymenu:
@@ .. @@
     def menu(self):
         options = {
-            'Soon': lambda: (self.logger.log('Coming soon'))[0],
+            'Funny Stuff': funnystuff().menu,
         }