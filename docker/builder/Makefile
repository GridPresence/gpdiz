TARGET = builder
RETARGET = ${TARGET}-${PLATFORM_ARCH}
BLDR_BUILD := ../../build
LOG_FILE := ${BLDR_BUILD}/${TARGET}_build.log
DKR_LOG_OPT := 2>&1 | tee -a ${LOG_FILE}
DKR_BLD_OPTIONS := --rm ${DKR_BLD_OPTIONS}
#ECR_ACCT := 245152938451
#ECR_REG := us-west-2
#ECR_URI := ${ECR_ACCT}.dkr.ecr.${ECR_REG}.amazonaws.com
#SRC_PACKAGE := ${BLDR_BUILD}/${TARGET}.zip 
#HARDV := 0.0.2

.PHONY: clean
clean:
	rm -fr ${SRC_PACKAGE}
	rm -fr ${LOG_FILE}
	mkdir -p ${BLDR_BUILD}

.PHONY: check
check: clean
	docker build ${DKR_BLD_OPTIONS} -f Dockerfile -t ${TARGET} . ${DKR_LOG_OPT}
	docker tag ${TARGET} ${TARGET}:latest

# .PHONY: deploy
# deploy: clean check
# 	aws ecr get-login-password --region ${ECR_REG} | docker login --username AWS --password-stdin ${ECR_URI}
# 	docker tag ${TARGET}:latest ${ECR_URI}/${RETARGET}
# 	docker push ${ECR_URI}/${RETARGET}:latest


