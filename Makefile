.PHONY: all
all: clean-rpm build-rpm check-rpm

.PHONY:
clean-rpm:
	rm -rf BUILD RPMS

.PHONY: build-rpm
build-rpm:
	rpmbuild \
		--noclean \
		--define "_topdir $(shell pwd)" \
		--define "_srcrpmdir $(shell pwd)" \
		--define "_sourcedir $(shell pwd)" \
		-ba annobin-test.spec

.PHONY: check-rpm
check-rpm:
	annocheck \
		--verbose \
		--skip-pie \
		RPMS/x86_64/annobin-test-1.0.0-1.*.x86_64.rpm
