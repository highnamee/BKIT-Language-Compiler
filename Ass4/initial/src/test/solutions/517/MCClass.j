.source MCClass.java
.class public MCClass
.super java.lang.Object
.field static x F
.field static y I

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
Label0:
	getstatic MCClass/x F
	getstatic MCClass/y I
	i2f
	fcmpl
	ifle Label2
	iconst_1
	goto Label3
Label2:
	iconst_0
Label3:
	ifle Label4
	iconst_1
	ifle Label4
	iconst_1
	goto Label5
Label4:
	iconst_0
Label5:
	ifgt Label7
	iconst_0
	ifgt Label7
	iconst_0
	goto Label6
Label7:
	iconst_1
Label6:
	invokestatic io/string_of_bool(Z)Ljava/lang/String;
	invokestatic io/print(Ljava/lang/String;)V
Label1:
	return
.limit stack 11
.limit locals 1
.end method

.method public <clinit>()V
	ldc 2.0
	putstatic MCClass/x F
	iconst_3
	putstatic MCClass/y I
	return
.limit stack 1
.limit locals 0
.end method

.method public <init>()V
.var 0 is this LMCClass; from Label0 to Label1
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
Label1:
	return
.limit stack 1
.limit locals 1
.end method
