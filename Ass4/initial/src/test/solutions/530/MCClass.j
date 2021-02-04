.source MCClass.java
.class public MCClass
.super java.lang.Object

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
.var 1 is x I from Label0 to Label1
	iconst_3
	istore_1
Label0:
	iload_1
	iconst_1
	if_icmpne Label6
	iconst_1
	goto Label7
Label6:
	iconst_0
Label7:
	ifle Label2
	ldc "1"
	invokestatic io/print(Ljava/lang/String;)V
	goto Label5
Label2:
	iload_1
	iconst_2
	if_icmpne Label8
	iconst_1
	goto Label9
Label8:
	iconst_0
Label9:
	ifle Label3
	ldc "2"
	invokestatic io/print(Ljava/lang/String;)V
	goto Label5
Label3:
	iload_1
	iconst_3
	if_icmpne Label10
	iconst_1
	goto Label11
Label10:
	iconst_0
Label11:
	ifle Label4
	ldc "3"
	invokestatic io/print(Ljava/lang/String;)V
	goto Label5
Label4:
	ldc "Do_not_know"
	invokestatic io/print(Ljava/lang/String;)V
Label5:
	ldc " Out"
	invokestatic io/print(Ljava/lang/String;)V
Label1:
	return
.limit stack 7
.limit locals 2
.end method

.method public <clinit>()V
	return
.limit stack 0
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
